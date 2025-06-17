# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/03 11:13:28 by dfine             #+#    #+#              #
#    Updated: 2025/05/18 13:47:35 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from fastapi import FastAPI

from tools.routes import asset, chat, consumer, doc_parse


app = FastAPI()
app.include_router(chat.router)
app.include_router(consumer.router)
app.include_router(doc_parse.router)
app.include_router(asset.router)
