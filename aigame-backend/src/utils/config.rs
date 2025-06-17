// ************************************************************************** //
//                                                                            //
//                                                        :::      ::::::::   //
//   config.rs                                          :+:      :+:    :+:   //
//                                                    +:+ +:+         +:+     //
//   By: dfine <coding@dfine.tech>                  +#+  +:+       +#+        //
//                                                +#+#+#+#+#+   +#+           //
//   Created: 2025/03/20 20:09:38 by dfine             #+#    #+#             //
//   Updated: 2025/04/15 15:08:49 by dfine            ###   ########.fr       //
//                                                                            //
// ************************************************************************** //

use dotenvy::dotenv;
use std::env;

use super::message_queue::StreamObj;
pub struct Config {
    database_uri: String,
    parse_stream_obj: StreamObj,
    game_stream_obj: StreamObj,
}

impl Config {
    pub async fn init() -> Self {
        let _ = dotenv();
        let database_uri = env::var("DATABASE_URL")
            .unwrap_or("mysql://creator:creator-25@aigame-mysql:3306/aigame".to_string());
        let rabbitmq_host = env::var("RABBITMQ_HOST").unwrap_or("rabbitmq".to_string());
        let rabbitmq_username = env::var("RABBITMQ_USERNAME").unwrap_or("aigame".to_string());
        let rabbitmq_password = env::var("RABBITMQ_PASSWORD").unwrap_or("aigame-25".to_string());
        let rabbitmq_parse_name =
            env::var("RABBITMQ_PARSE_NAME").unwrap_or("aigame-parse".to_string());
        let rabbitmq_game_name =
            env::var("RABBITMQ_GAME_NAME").unwrap_or("aigame-game".to_string());
        let parse_stream_obj = StreamObj::new(
            &rabbitmq_host,
            &rabbitmq_username,
            &rabbitmq_password,
            rabbitmq_parse_name,
        )
        .await;
        let game_stream_obj = StreamObj::new(
            &rabbitmq_host,
            &rabbitmq_username,
            &rabbitmq_password,
            rabbitmq_game_name,
        )
        .await;
        Self {
            database_uri,
            parse_stream_obj,
            game_stream_obj,
        }
    }

    pub fn database_uri(&self) -> &str {
        self.database_uri.as_str()
    }

    pub fn parse_stream_obj(&self) -> &StreamObj {
        &self.parse_stream_obj
    }
    pub fn game_stream_obj(&self) -> &StreamObj {
        &self.game_stream_obj
    }
}
