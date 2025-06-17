# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    consumer.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/03 11:12:44 by dfine             #+#    #+#              #
#    Updated: 2025/05/14 15:27:29 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from faststream.rabbit import QueueType, RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter
from loguru import logger
from pamqp.common import FieldTable

from tools import FILE_SERVER_PREFIX, RABBITMQ_MAX_CONSUMER
from tools.definitions import (
    GameGoalElement,
    GameHandlerPayload,
    GamePlanModel,
    PptHandlerPayload,
    PptInfo,
    message_config,
)
from tools.dependencies import (
    PptParseRequest,
    create_game,
    delete_game_by_attach_id,
    ppt_parse,
    query_attach_status,
    query_game_status,
    update_attach_status,
    update_game_status,
)
from tools.instances import code_agent

client_properties: FieldTable = {
    "name": "aigame-tools-consumer",
    "heartbeat": 30,
    "connection_timeout": 3600000,
    "consumer-timeout": 3600000,
}
router = RabbitRouter(
    url=message_config.uri,
    max_consumers=RABBITMQ_MAX_CONSUMER,
    client_properties=client_properties,
)

custom_args: Any = {
    "x-queue-leader-locator": "least-leaders",
}
parse_queue = RabbitQueue(
    name=message_config.queue_name.ppt_parse,
    durable=True,
    queue_type=QueueType.STREAM,
    arguments=custom_args,
)

game_queue = RabbitQueue(
    name=message_config.queue_name.game_generate,
    durable=True,
    queue_type=QueueType.STREAM,
    arguments=custom_args,
)


async def ppt_parse_process(
    id: int,
    path: str,
):
    if not update_attach_status(id, "parsing"):
        return
    ppt_parse_request = PptParseRequest(ppt_file=path)
    try:
        parse_result = await ppt_parse(ppt_parse_request)
        if parse_result.result is None or parse_result.status != "succeed":
            logger.error(f"parse ppt failed: {parse_result = }")
            return
        project_path = Path(path).parent
        logger.info(f"ppt parsed:\n {parse_result}")
        with open(project_path / "parse.json", "w") as f:
            _ = f.write(parse_result.result.model_dump_json())
        logger.info(f"saving parse result to {project_path}/parse.json")
        logger.info(f"process finished, result: {parse_result}")
        if not update_attach_status(
            id,
            "parse",
        ):
            return
    except Exception as e:
        logger.error(f"parse failed: {e}")
        if not update_attach_status(id, "fparse"):
            return


async def goal_list_generate(
    id: int,
    project_path: Path,
):
    try:
        parse_result = PptInfo.model_validate(
            json.loads((project_path / "parse.json").read_text(encoding="utf-8"))
        )
        logger.info("goal generating...")
        goal = await code_agent.goal(parse_result)
        if goal is None:
            logger.error("failed to generate goal")
            if not update_attach_status(
                id,
                "fgoal",
            ):
                logger.error(f"update attach status failed, attach id: {id}")
            return
        for module_id, each_goal in enumerate(goal.modules):
            game_key = uuid4()
            game_path = Path(f"/data/download/game/{game_key}")
            game_path.mkdir(parents=True, exist_ok=True)
            with open(game_path / "goal.json", "w") as f:
                _ = f.write(each_goal.model_dump_json())
            logger.info(f"saving goals to {game_path}/goals.json")
            if not create_game(
                id,
                "goal",
                module_id,
                str(game_key),
            ):
                return
        if not update_attach_status(
            id,
            "goal",
        ):
            logger.error(f"update attach status failed, attach id: {id}")
    except Exception as e:
        logger.error(f"failed to generate goal, error: {e}")
        if not update_attach_status(
            id,
            "fgoal",
        ):
            logger.error(f"update attach status failed, attach id: {id}")


async def goal_generate_standalone(
    id: int,
    project_path: Path,
):
    try:
        parse_result = PptInfo.model_validate(
            json.loads((project_path / "parse.json").read_text(encoding="utf-8"))
        )
        logger.info("goal generating standalone...")
        for module_id, slide_module in parse_result.get_a_module():
            if module_id == 0:
                continue
            logger.info(f"goal generating => {module_id= }")
            goal = await code_agent.each_module_goal(slide_module)
            if goal is None:
                logger.error("failed to generate goal")
                if not update_attach_status(
                    id,
                    "fgoal",
                ):
                    logger.error(f"update attach status failed, attach id: {id}")
                return
            game_key = uuid4()
            game_path = Path(f"/data/download/game/{game_key}")
            game_path.mkdir(parents=True, exist_ok=True)
            with open(game_path / "goal.json", "w") as f:
                _ = f.write(goal.model_dump_json())
            logger.info(f"saving goals to {game_path}/goals.json")
            if not create_game(
                id,
                "goal",
                module_id,
                str(game_key),
            ):
                return
        if not update_attach_status(
            id,
            "goal",
        ):
            logger.error(f"update attach status failed, attach id: {id}")
    except Exception as e:
        logger.error(f"failed to generate goal, error: {e}")
        if not update_attach_status(
            id,
            "fgoal",
        ):
            logger.error(f"update attach status failed, attach id: {id}")


async def goal_generate(
    id: int,
    path: str,
):
    project_path = Path(path).parent
    # goal generate
    try:
        parse_result = PptInfo.model_validate(
            json.loads((project_path / "parse.json").read_text(encoding="utf-8"))
        )
        if parse_result.document_info[0].module_id is not None:
            return await goal_generate_standalone(id=id, project_path=project_path)
        logger.warning("No level was manually assigned")
        return await goal_list_generate(id=id, project_path=project_path)
    except Exception as e:
        logger.error(f"failed to parse ppt info, error: {e}")


async def plan_generate(
    id: int,
    game_path: Path,
):
    if not update_game_status(
        id,
        status="planing",
    ):
        return
    try:
        goal = GameGoalElement.model_validate(
            json.loads((game_path / "goal.json").read_text(encoding="utf-8"))
        )
        # plan generate
        logger.info("plan generating...")
        plan = await code_agent.plan(goal)
        if plan is None:
            logger.error("failed to generate plan")
            if not update_game_status(
                id,
                "fplan",
            ):
                return
            return
        with open(game_path / "plan.json", "w") as f:
            _ = f.write(plan.model_dump_json())
        logger.info(f"saving plan to {game_path}/plan.json")
        if not update_game_status(
            id,
            "plan",
        ):
            return
    except Exception as e:
        logger.error(f"failed to generate plan, error: {e}")
        if not update_game_status(
            id,
            "fplan",
        ):
            logger.error(f"update game status failed, attach id: {id}")


async def code_generate(
    id: int,
    game_path: Path,
):
    if not update_game_status(
        id,
        "coding",
    ):
        return
    try:
        plan = GamePlanModel.model_validate(
            json.loads((game_path / "plan.json").read_text(encoding="utf-8"))
        )

        code = await code_agent.code(plan=plan)
        if code is None:
            if not update_game_status(
                id,
                "fcode",
            ):
                return
            logger.error("failed to generate game code")
            return
        logger.info(f"code generated: {code}")
        logger.info(f"code has saved to: {game_path}/App.tsx")
        with open(f"{game_path}/App.tsx", "w") as f:
            _ = f.write(code)
        html_code = await code_agent.code_html(plan=plan)
        logger.info(f"html code generated: {html_code}")
        if html_code is not None:
            with open(f"{game_path}/index.html", "w") as f:
                _ = f.write(html_code)
            logger.info(f"html code has saved to: {game_path}/index.html")
        logger.info("checking code...")
        check_result = await code_agent.check_code(game_path / "App.tsx")
        if not check_result:
            logger.error("can not correct the code use ai.")
        if not update_game_status(
            id, "code", access_url=f"{FILE_SERVER_PREFIX}{game_path}/index.html"
        ):
            return
    except Exception as e:
        logger.error(f"failed to generate code, error: {e}")
        if not update_game_status(
            id,
            "fcode",
        ):
            logger.error(f"update game status failed, attach id: {id}")


@router.subscriber(
    parse_queue,
    consume_args={
        "x-stream-offset": "next",
    },
    retry=3,
)
async def ppt_handler(
    mq_payload: PptHandlerPayload,
):
    id, path = mq_payload.id, mq_payload.path
    logger.info(f"parsing ppt: {id}, path: {path}")
    attach_status = query_attach_status(
        id,
    )
    match attach_status:
        case "uploaded" | "fparse":
            await ppt_parse_process(
                id,
                path,
            )
        case "parse":
            await goal_generate(
                id,
                path,
            )
        case "fgoal" | "goal":
            if not delete_game_by_attach_id(id):
                logger.error(f"failed to delete game for ppt {id}")
                return
            await goal_generate(
                id,
                path,
            )
        case _:
            logger.error("invalid ppt status!")


# status: goal->plan-> code
async def generate_pipe(
    id: int,
    file_key: str,
):
    status = query_game_status(id)
    if status is None:
        logger.error("failed to query game case status")
        return
    logger.info(f"generating pipe, {id = }, {file_key = }, {status = }")
    game_path = Path(f"/data/download/game/{file_key}")
    if not game_path.exists():
        logger.error(f"game path {game_path} not exist!")
        return
    match status:
        case "goal" | "fplan":
            await plan_generate(
                id,
                game_path,
            )
        case "plan" | "code" | "fcode":
            await code_generate(
                id,
                game_path,
            )
        case _:
            logger.error("invalid status")
    logger.info("msg consumed")


@router.subscriber(
    game_queue,
    consume_args={
        "x-stream-offset": "next",
    },
    retry=3,
)
async def game_generator(
    mq_payload: GameHandlerPayload,
):
    await generate_pipe(mq_payload.id, mq_payload.file_key)
