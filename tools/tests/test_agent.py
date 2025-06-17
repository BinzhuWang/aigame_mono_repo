import json
from pathlib import Path

from tools.definitions import GameGoalOutput, GamePlanModels
from tools.game_agent import CodeAgent


async def test_plan():
    code_agent = CodeAgent()
    goal = GameGoalOutput.model_validate(
        json.loads(Path("tests/goal.json").read_text(encoding="utf-8"))
    )
    plan = await code_agent.plan(goal)
    assert plan is not None


async def test_code():
    code_agent = CodeAgent()
    plan = GamePlanModels.model_validate(
        json.loads(Path("tests/plan.json").read_text(encoding="utf-8"))
    )
    code = await code_agent.create_code(plan)
    assert code is not None
