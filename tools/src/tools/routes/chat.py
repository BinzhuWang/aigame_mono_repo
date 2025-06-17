# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    chat.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/06 16:19:34 by dfine             #+#    #+#              #
#    Updated: 2025/05/06 16:19:35 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel

from tools.definitions import ChatContentModel, ResponseModel
from tools.instances import code_agent
from loguru import logger

router = APIRouter()


class ChatModel(BaseModel):
    game_path: str
    content: list[ChatContentModel]


@router.post("/chat")
async def code_chat(chat_info: ChatModel) -> ResponseModel:
    try:
        game_path = Path(chat_info.game_path)
        res_code = await code_agent.modify_code(
            game_path=game_path, modify_info=chat_info.content
        )
        if res_code:
            return ResponseModel(
                msg="chat with code finished.", result={"code": res_code}
            )
    except (ValueError, IOError, TypeError) as err:
        logger.error(f"cannot chat with code. {err= }")
    return ResponseModel(msg="chat with code failed.", status="failed", code=500)
