# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    doc_parse.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/03 11:13:36 by dfine             #+#    #+#              #
#    Updated: 2025/04/03 11:13:37 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from fastapi import APIRouter

from tools.definitions import PptResponseModel

from ..dependencies import (
    PptParseRequest,
    ppt_parse,
    query_openai_client,
)

router = APIRouter()


@router.get("/query_agent")
async def query_agent():
    await query_openai_client()


@router.post("/ppt_parse")
async def ppt_parse_router(item: PptParseRequest) -> PptResponseModel:
    return await ppt_parse(item)
