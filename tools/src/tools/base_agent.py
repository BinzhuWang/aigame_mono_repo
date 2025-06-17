# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    base_agent.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/11 11:33:58 by dfine             #+#    #+#              #
#    Updated: 2025/05/12 11:43:35 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
from typing import TypeAlias
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.settings import ModelSettings
from . import (
    ANTHROPIC_API_KEY,
    DENO_PATH,
    LLM_MAX_TOKEN,
    MODEL_PROVIDER,
    OPENAI_BASE_URL,
    OPENAI_API_KEY,
    BASE_MODEL,
)

ProviderType: TypeAlias = OpenAIProvider | AnthropicProvider
ModelType: TypeAlias = OpenAIModel | AnthropicModel


class BaseAgent:
    provider: ProviderType
    model: ModelType
    model_setting: ModelSettings
    fs_server: MCPServerStdio
    asset_server: MCPServerStdio

    def _get_model_instance(self, model_name: str) -> ModelType:
        if isinstance(self.provider, AnthropicProvider):
            return AnthropicModel(model_name, provider=self.provider)
        return OpenAIModel(model_name, provider=self.provider)

    def __init__(self):
        match MODEL_PROVIDER:
            case "anthropic":
                self.provider = AnthropicProvider(api_key=ANTHROPIC_API_KEY)
            case _:
                self.provider = OpenAIProvider(
                    base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY
                )
        self.model = self._get_model_instance(BASE_MODEL)

        self.model_setting = ModelSettings(
            max_tokens=int(LLM_MAX_TOKEN), temperature=0.5
        )
        self.fs_server = MCPServerStdio(
            DENO_PATH,
            args=[
                "run",
                "-A",
                "npm:@modelcontextprotocol/server-filesystem",
                "/data",
            ],
        )
        self.asset_server = MCPServerStdio(
            command="uv",
            args=["run", "-m", "tools.mcp_server.asset.asset_server", "server"],
            env=os.environ.copy(),
        )
