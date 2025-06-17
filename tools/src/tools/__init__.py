# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/03 11:13:46 by dfine             #+#    #+#              #
#    Updated: 2025/05/12 11:43:23 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os

from dotenv import load_dotenv

_ = load_dotenv()
DOCUMENT_API = os.getenv(
    "DOCUMENT_SERVER_URL", "http://documentserver/ConvertService.ashx"
)
SERVER_PREFIX = "http://aigame-backend:8080"
FILE_SERVER_PREFIX = os.getenv(
    "SERVER_DOMAIN", "https://api.gamecreator.online"
).rstrip("/")
DOC_SERV_JWT_SECRET = "aigame"
STATIC_DIR = "/data/upload/"
AUDIO_LIB_DIR = os.getenv("AUDIO_LIB_DIR", "/data/static/audio_lib")
BASE_MODEL = os.getenv("BASE_MODEL", "claude-3-7-sonnet-20250219-thinking")
GOAL_MODEL = os.getenv("GOAL_MODEL", "claude-3-7-sonnet-20250219-thinking")
PLAN_MODEL = os.getenv("PLAN_MODEL", "gpt-4o")
TAG_MODEL = os.getenv("PLAN_MODEL", "gpt-4o")
RABBITMQ_URI = os.getenv("RABBITMQ_URI", "amqp://aigame:aigame-25@rabbitmq:5672/")
RABBITMQ_PARSE_QUEUE = os.getenv("RABBITMQ_PARSE_QUEUE", "aigame-parse")
RABBITMQ_GEN_QUEUE = os.getenv("RABBITMQ_GEN_QUEUE", "aigame-game")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "aigame-exchange")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY", "aigame-routing-key")
RABBITMQ_MAX_CONSUMER = int(os.getenv("RABBITMQ_MAX_CONSUMER", 1))
GATEWAY = os.getenv("GATEWAY_URL", "http://aigame-backend:8080")
CODESAVEDIR = os.getenv("CODESAVEDIR", "uploads/code/")
DENO_PATH = os.getenv("DENO_PATH", "/root/.deno/bin/deno")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MAX_TOKEN = os.getenv("LLM_MAX_TOKEN", "12800")
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY", "")
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "aigame-25")
TMP_DIR = os.getenv("TMP_DIR", "/data/tmp")
