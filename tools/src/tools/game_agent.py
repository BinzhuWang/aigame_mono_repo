# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    game_agent.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/09 13:15:57 by dfine             #+#    #+#              #
#    Updated: 2025/05/14 14:20:57 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re
from pathlib import Path

from loguru import logger
from pydantic_ai import Agent
from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_fixed,
)
from tqdm.asyncio import tqdm

from prompts import shadcn
from tools import AUDIO_LIB_DIR, GOAL_MODEL, PLAN_MODEL
from tools.deno_lint import lint
from tools.dependencies import (
    count_tokens,
    feedback_desp,
    from_ppt_slide_list,
    module_filter,
    ppt_filter,
)
from tools.generate_audio_lib import generate_lib

from .base_agent import BaseAgent, ModelType
from .definitions import (
    ChatContentModel,
    GameDesignModule,
    GameGoalElement,
    GameGoalList,
    GamePlanModel,
    GamePlanModels,
    GameProjectModel,
    GameTaskModel,
    PptInfo,
    PptSlideList,
)
from .wrap_funcs import get_time_async

InputModel = (
    GameGoalElement
    | GameGoalList
    | GameDesignModule
    | GamePlanModels
    | GameTaskModel
    | GameProjectModel
)

OutputModel = (
    GameGoalList
    | GameDesignModule
    | GamePlanModel
    | GamePlanModels
    | GameTaskModel
    | GameProjectModel
    | str
    | None
)


def is_none(result: OutputModel) -> bool:
    return result is None


def is_false(result: bool) -> bool:
    return not result


class CodeAgent(BaseAgent):
    code_type: str
    goal_prompt: str
    goal_list_prompt: str
    plan_prompt: str
    plans_prompt: str
    coder_prompt: str
    lint_prompt: str
    merge_prompt: str
    goal_agent: Agent
    goal_list_agent: Agent
    plan_agent: Agent
    plans_agent: Agent
    code_agent: Agent
    lint_agent: Agent
    merge_agent: Agent
    plan_model: ModelType
    goal_model: ModelType
    plans_model: ModelType

    def __init__(self, code_type: str = "tsx"):
        super().__init__()
        self.code_type = code_type
        self.goal_prompt = self.__read_prompt("prompts/goal.p")
        self.goal_list_prompt = self.__read_prompt("prompts/goal_list.p")
        self.plan_prompt = self.__read_prompt("prompts/plan.p")
        self.plans_prompt = self.__read_prompt("prompts/plans.p")
        self.merge_prompt = self.__read_prompt("prompts/merge.p")
        self.lint_prompt = self.__read_prompt("prompts/lint.p")
        self.coder_prompt = shadcn.system_prompt

        self.goal_model = self._get_model_instance(GOAL_MODEL)
        self.plan_model = self._get_model_instance(PLAN_MODEL)
        self.plans_model = self._get_model_instance(PLAN_MODEL)

        self.goal_agent = Agent(self.goal_model, system_prompt=self.goal_prompt)
        self.goal_list_agent = Agent(
            self.goal_model, system_prompt=self.goal_list_prompt
        )
        self.plan_agent = Agent(
            self.plan_model,
            mcp_servers=[self.asset_server],
            system_prompt=self.plan_prompt,
        )
        self.plans_agent = Agent(
            self.plan_model,
            mcp_servers=[self.asset_server],
            system_prompt=self.plans_prompt,
        )
        self.code_agent = Agent(
            self.model,
            system_prompt=self.coder_prompt,
        )
        self.lint_agent = Agent(
            self.model,
            system_prompt=self.lint_prompt,
        )
        self.merge_agent = Agent(self.model, system_prompt=self.merge_prompt)
        # logger.info model info
        logger.info(
            f"current use model:\n\tname: {self.model.model_name}\n\tmax_tokens:{self.model_setting.get('max_tokens')}\n\ttemperature:{self.model_setting.get('temperature')}"
        )

    def __read_prompt(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _extract_code_pattern(self, code: str, code_pattern: str) -> str | None:
        match_case = re.search(code_pattern, code, re.DOTALL)
        return match_case.group(1) if match_case else None

    @retry(
        retry=retry_if_result(is_none) | retry_if_exception_type(),
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
    )
    @get_time_async
    async def each_module_goal(
        self, slide_list: PptSlideList
    ) -> GameGoalElement | None:
        llm_slide_list = from_ppt_slide_list(module_filter(slide_list))
        logger.info(llm_slide_list)
        token_count = count_tokens(llm_slide_list.model_dump_json())
        logger.info(f"this module input takes token counts is {token_count}")
        result = await self.goal_agent.run(llm_slide_list.model_dump_json())
        raw_agent_output = result.data
        match_case = re.search(
            r"```json\s*(.*?)```(?!.*```json)", raw_agent_output, re.DOTALL
        )
        if not match_case:
            return None
        json_str = match_case.group(1)
        logger.info(f"{json_str = }")
        try:
            return GameGoalElement.model_validate_json(json_data=json_str)
        except Exception as e:
            logger.error(
                f"[Validation Error] JSON 不符合 GameGoalOutput 结构：{e}\n{result.data}"
            )
            return None

    @retry(
        retry=retry_if_result(is_none) | retry_if_exception_type(),
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
    )
    @get_time_async
    async def goal(self, ppt_json: PptInfo) -> GameGoalList | None:
        """
        generate goal list from ppt parse json

        """
        ppt_filter_json = ppt_filter(ppt_json)
        token_count = count_tokens(ppt_filter_json.model_dump_json())
        logger.info(f"this goal list input takes token counts is {token_count}")
        result = await self.goal_list_agent.run(ppt_filter_json.model_dump_json())
        raw_agent_output = result.data
        # --- 修改正则以匹配最后一个 ```json ... ``` 块 ---
        logger.info(f"response for goal list, raw data:\n{result.data}")
        match_case = re.search(
            r"```json\s*(.*?)```(?!.*```json)", raw_agent_output, re.DOTALL
        )
        if not match_case:
            return None
        json_str = match_case.group(1)
        logger.info(f"{json_str = }")
        try:
            return GameGoalList.model_validate_json(json_data=json_str)
        except Exception as e:
            logger.error(
                f"[Validation Error] JSON 不符合 GameGoalOutput 结构：{e}\n{result.data}"
            )
            return None

    @retry(
        retry=retry_if_result(is_none) | retry_if_exception_type(),
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
    )
    @get_time_async
    async def plan(self, goal: GameGoalElement) -> GamePlanModel | None:
        async with self.plan_agent.run_mcp_servers():
            result = await self.plan_agent.run(goal.model_dump_json())
        match_case = re.search(r"```json\s*(.*?)```", result.data, re.DOTALL)
        json_str = match_case.group(1) if match_case else result.data
        try:
            return GamePlanModel.model_validate_json(json_data=json_str)
        except Exception as e:
            logger.error(
                f"[Validation Error] JSON 不符合 GameGoalOutput 结构：{e}\n{result.data}"
            )
            return None

    @retry(
        retry=retry_if_result(is_none) | retry_if_exception_type(),
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
    )
    async def plans(self, goal: GameGoalList) -> GamePlanModels | None:
        async with self.plans_agent.run_mcp_servers():
            result = await self.plans_agent.run(goal.model_dump_json())
        match_case = re.search(r"```json\s*(.*?)```", result.data, re.DOTALL)
        json_str = match_case.group(1) if match_case else result.data
        try:
            return GamePlanModels.model_validate_json(json_data=json_str)
        except Exception as e:
            logger.error(
                f"[Validation Error] JSON 不符合 GameGoalOutput 结构：{e}\n{result.data}"
            )
            return None

    @retry(
        retry=retry_if_result(is_none) | retry_if_exception_type(),
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
    )
    @get_time_async
    async def code_html(self, plan: GamePlanModel) -> str | None:
        audio_lib = generate_lib(Path(AUDIO_LIB_DIR))
        prompt = f"""
        Create an engaging interactive educational game for children and output the code with ```html ``` wrap.
        Each level will include interactive activities designed to help children learn and find enjoyment through education. The game flow should support the following stages: Start, Gameplay, and End. Each level must include:
        1. **Game Design**  
           The game should be captivating, featuring vibrant backgrounds, animations, and sounds. It should require players to mimic physical activities shown on screen, such as jumping, running, or kicking.
        2. **Assets**  
           Utilize a variety of resources such as background images, motion animations, and audio feedback to enhance the learning experience.

        Here is the input json, remember to use the asset.\n ```json\n{plan.model_dump_json()}\n```
        Here is the audio library in JSON. Please use suitable audio clips for buttons, feedback, background music, etc., and reference them in the code where appropriate:\n```json\n{audio_lib.model_dump_json()}\n```
        """
        logger.info(f"current input token ~= {count_tokens(prompt)}")
        result = await self.code_agent.run(prompt, model_settings=self.model_setting)
        html_code = self._extract_code_pattern(result.data, r"```html(.*?)```")
        logger.info(f"current level code:\n{html_code}")
        return html_code

    @retry(
        retry=retry_if_result(is_none) | retry_if_exception_type(),
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
    )
    @get_time_async
    async def code(self, plan: GamePlanModel) -> str | None:
        audio_lib = generate_lib(Path(AUDIO_LIB_DIR))
        prompt = f"""
        Create an engaging interactive educational game for children and output the code with ```tsx ``` wrap.
        Each level will include interactive activities designed to help children learn and find enjoyment through education. The game flow should support the following stages: Start, Gameplay, and End. Each level must include:
        1. **Game Design**  
           The game should be captivating, including backgrounds, animations, and sounds.
        2. **Assets**  
           Utilize a variety of resources such as background images, motion animations, and audio feedback to enhance the learning experience.

        Here is the input requirement and asset, remember to use the asset.\n ```json\n{plan.model_dump_json()}\n```
        Here is the audio library in JSON. Please use suitable audio clips for buttons, feedback, background music, etc., and reference them in the code where appropriate:\n```json\n{audio_lib.model_dump_json()}\n```
        """
        logger.info(f"current input token ~= {count_tokens(prompt)}")
        result = await self.code_agent.run(prompt, model_settings=self.model_setting)
        ts_code = self._extract_code_pattern(result.data, r"```tsx\n(.*?)```")
        logger.info(f"current level code:\n{ts_code}")
        return ts_code

    @retry(
        retry=retry_if_result(is_false) | retry_if_exception_type(),
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
    )
    @get_time_async
    async def check_code(self, code_path: Path) -> bool:
        lint_res, lint_err = lint(code_path)
        if lint_res is None or lint_err is not None:
            logger.error(f"failed to lint code, err: {lint_err}")
            return False
        logger.info(f"code lint result is:\n{lint_res.model_dump_json()}")
        if len(lint_res.diagnostics) == 0 and len(lint_res.errors) == 0:
            logger.info("code is correct")
            return True
        prompt = f"""
        Please correct the code from `App.tsx`, the original code is:\n```tsx{code_path.read_text(encoding="utf-8")}```\nthe lint json is:\n```json{lint_res.model_dump_json()}```
        """
        logger.info(f"current input token ~= {count_tokens(prompt)}")
        result = await self.lint_agent.run(prompt, model_settings=self.model_setting)
        ts_code = self._extract_code_pattern(result.data, r"```tsx\n(.*?)```")
        if ts_code is None:
            logger.error("empty code generate")
            return False
        logger.info(f"modified code according to lint result:\n{ts_code}")
        with open(code_path, "w") as f:
            _ = f.write(ts_code)
        return True

    async def _code_with_combined(self, plan: GamePlanModels) -> str | None:
        prompt = f"""
        按要求为儿童创建一个有意思的互动教育游戏。
        每个关卡将包含交互式活动，旨在帮助儿童在教育中学习并找到乐趣。游戏流程应支持以下阶段：开始、游戏、结束。每个关卡必须包括：
        1. 游戏设计：游戏应该引人入胜，具有鲜艳的背景、动画和声音。
        2. 资源：利用各种资源，如背景图片、动作动画和音频反馈，以增强学习体验。
        3. 原型流程：游戏流程应遵循以下模式：
        4. 开始：显示一个带有吸引人动画的开始按钮。
        5. 游戏：玩家按照指示执行动作。
        6. 结束：玩家收到反馈，并可选择重试或进入下一个活动。
        以下是游戏的设计需求信息，记得使用其中的资源。\n ```json\n${plan.model_dump_json()}\n```
        """
        match self.code_type:
            case "html":
                prompt += """请详细思考和设计后并考虑UI美观程度，将所有的实现都放在一个完整的html代码中(包含必要的CDN链接，比如React、ReactDOM、Babel等），并以script标签的形式包含TSX代码，最终生成html文件，各个描述均以英文展示，以```html开头，以```结尾。"""
            case _:
                prompt += """请先详细思考和设计，并考虑UI美观程度（思考过程用<think></think>标签包裹），给出一个完整的tsx代码，各个描述均以英文展示，记得代码一定要以```tsx开头，以```结尾！！！"""
        logger.info(f"current input token ~= {count_tokens(prompt)}")
        result = await self.code_agent.run(prompt, model_settings=self.model_setting)
        ts_code = self._extract_code_pattern(result.data, r"```tsx\n(.*?)```")
        # TODO add func for tsx code validation
        return ts_code

    @retry(
        retry=retry_if_result(is_none) | retry_if_exception_type(),
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
    )
    async def create_code(
        self, plans: GamePlanModels, split_level: bool = False
    ) -> str | None:
        logger.info(
            f"generating code now, the code file type is: {self.code_type}, split each level:{split_level}"
        )
        if not split_level:
            return await self._code_with_combined(plans)
        level_codes = [
            code
            for plan in tqdm(plans.root, desc="Processing levels", dynamic_ncols=True)
            if (code := await self.code(plan)) is not None
        ]

        logger.info(f"this game contains {len(level_codes)} levels")
        prompt = f"""
        here is each level code list, please merge them to a single tsx file.\n {level_codes}\n```
        """
        logger.info(f"{prompt= }")
        logger.info(f"current input token ~= {count_tokens(prompt)}")
        result = await self.merge_agent.run(prompt, model_settings=self.model_setting)
        ts_code = self._extract_code_pattern(result.data, r"```tsx\n(.*?)```")
        return ts_code

    @retry(
        retry=retry_if_result(is_none) | retry_if_exception_type(),
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
    )
    @get_time_async
    async def modify_code(
        self,
        game_path: Path,
        modify_info: list[ChatContentModel],
        use_b64_image: bool = False,
    ) -> str | None:
        """
        修改代码
            game_path: 游戏目录
            modify_info: list[ChatContentModel](ChatContentModel:
                feedback_type: 反馈类型：sandbox debug/user ask/screenshot
                content: 反馈内容，根据反馈类型可能是debug信息，用户提问，或者截图的b64 string
                )
        """
        if len(modify_info) == 0:
            logger.info("empty modify info")
            return None
        with open(game_path / "App.tsx", "r") as f:
            code = f.read()
        # with open(game_path / "plan.json", "r") as f:
        #     plan= f.read()
        prompt = f"""请根据当前代码反馈修改代码，保证代码的完整性，按照要求优化游戏。 当前的代码：\n```tsx\n{code}```\n注意请给出完整的修改代码，即使无需改动的部分也请完整给出来，不要省略。"""
        for m in modify_info:
            if not use_b64_image:
                m = m.convert_b64_to_url()
            prompt += f"""来自{feedback_desp(m.feedback_type)}: {m.content}\n"""
        prompt += """请结合反馈，详细思考和设计后并考虑UI美观程度（思考过程用<think></think>标签包裹），给出修改后的**完整代码**，各个描述均以英文展示，代码内容以```tsx开头，以```结尾。"""
        logger.info(f"current input token ~= {count_tokens(prompt)}")
        result = await self.code_agent.run(prompt, model_settings=self.model_setting)
        ts_code = self._extract_code_pattern(result.data, r"```tsx\n(.*?)```")
        return ts_code
