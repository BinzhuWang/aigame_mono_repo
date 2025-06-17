import requests
import os
import sys
import json
import asyncio

from typer import Typer
from pathlib import Path

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.join(current_script_dir, os.pardir)
tools_dir = os.path.join(project_root_dir, "src")

sys.path.insert(0, project_root_dir)
sys.path.insert(0, tools_dir)

from tools.game_agent import CodeAgent  # noqa
from tools.definitions import GamePlanModels  # noqa
from tools.dependencies import login  # noqa

GATEWAY = "https://api.gamecreator.online"

cli = Typer()
jwt_token: str | None = None

code_agent = CodeAgent()


def download_file_from_url(url: str) -> str:
    """从URL下载计划内容"""
    print(f"检测到 HTTPS URL，尝试下载: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        plan_content = response.text
        print("下载成功。")
        return plan_content
    except requests.exceptions.RequestException as e:
        print(f"下载 {url} 时发生错误: {e}")
        raise e

def read_content_from_file(file_path: str) -> str:
    """从本地文件读取计划内容"""
    print(f"检测到本地文件路径，尝试读取: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print("本地文件读取成功。")
        return content
    except FileNotFoundError as e:
        print(f"错误：本地文件未找到，路径: {file_path}")
        raise e
    except IOError as e:
        print(f"读取本地文件 {file_path} 时发生 IO 错误: {e}")
        raise e

def get_content(path: str) -> str:
    """获取计划内容，支持URL或本地文件路径"""
    if path.startswith("https://"):
        return download_file_from_url(path)
    else:
        return read_content_from_file(path)

def save_content_to_file(content: str, output_dir: str):
    """保存内容到文件"""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    with open(out_path / "App.tsx", "w") as f:
        _ = f.write(content)
    print(f"内容已保存到 {out_path / 'App.tsx'}")

def update_content_to_server(content: str, update_id: int):
    """更新内容到服务器"""
    global jwt_token
    if not jwt_token:
        jwt_token = login(gateway=GATEWAY)
    response = requests.post(
        f"{GATEWAY}/game/module?id={update_id}&&module_type=code",
        data=content,
        headers={"Authorization": jwt_token},
    )
    if response.status_code == 200:
        print(f"update content to server(GATEWAY: {GATEWAY}/game/module?id={update_id}&&module_type=code) succeed. response: {response.json()}")
    else:
        print(f"update content to server(GATEWAY: {GATEWAY}/game/module?id={update_id}&&module_type=code) failed. msg: {response.text}")

@cli.command()
def code(
    content_path: str,
    update_id: int | None = None,
    combined: bool = False,
    output_dir: str = "tests",
):
    # 获取计划内容
    plan_content = get_content(content_path)
    
    # 解析计划模型
    plans = GamePlanModels.model_validate(json.loads(plan_content))
    
    # 生成代码
    res_code = asyncio.run(
        code_agent.create_code(plans=plans, split_level=not combined)
    )
    if not res_code:
        print("生成代码失败")
        return
    
    # 保存代码到文件
    save_content_to_file(res_code, output_dir)
    
    # 如果需要，更新代码到服务器
    if update_id:
        update_content_to_server(res_code, update_id)


@cli.command()
def modify_code(
    code_path: str,
    plan_path: str,
    feedback: str,
    modify_type: str,
    update_id: int | None = None,
    output_dir: str = "tests",
):
    # 获取计划内容
    plan_content = get_content(plan_path)
    code_content = get_content(code_path)
    # 解析计划模型
    plans = GamePlanModels.model_validate(json.loads(plan_content))
    
    # 修改代码
    res_code = asyncio.run(
        code_agent.modify_code(
            code=code_content, 
            plans=plans, 
            feedback=feedback,
            modify_type=modify_type
        )
    )
    if not res_code:
        print("修改代码失败")
        return
    
    # 保存代码到文件
    save_content_to_file(res_code, output_dir)
    
    # 如果需要，更新代码到服务器
    if update_id:
        update_content_to_server(res_code, update_id)  


if __name__ == "__main__":
    cli()
