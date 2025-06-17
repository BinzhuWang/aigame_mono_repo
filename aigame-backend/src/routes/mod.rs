// ************************************************************************** //
//                                                                            //
//                                                        :::      ::::::::   //
//   mod.rs                                             :+:      :+:    :+:   //
//                                                    +:+ +:+         +:+     //
//   By: dfine <coding@dfine.tech>                  +#+  +:+       +#+        //
//                                                +#+#+#+#+#+   +#+           //
//   Created: 2025/03/20 20:09:50 by dfine             #+#    #+#             //
//   Updated: 2025/04/15 17:26:55 by dfine            ###   ########.fr       //
//                                                                            //
// ************************************************************************** //

mod assets;
mod auth;
mod chat;
mod finder;
mod game;
mod proxy;
mod status;
mod tools;
mod types;
mod user;

use crate::utils::{config::Config, init};
use actix_cors::Cors;
use actix_files::Files;
use actix_web::{
    App, HttpServer,
    middleware::{self, from_fn},
    web,
};
use auth::auth_middleware;
use rabbitmq_stream_client::{NoDedup, Producer};
use sea_orm::DatabaseConnection;

#[derive(Clone)]
pub struct AppState {
    db: DatabaseConnection,
    parse_producer: Producer<NoDedup>,
    game_producer: Producer<NoDedup>,
}

pub async fn create_routes() -> std::io::Result<()> {
    let conf = Config::init().await;
    let db = init::init_db(conf.database_uri()).await.unwrap();
    let parse_producer = conf.parse_stream_obj().producer().await;
    let game_producer = conf.game_stream_obj().producer().await;
    let app_state = AppState {
        db,
        parse_producer,
        game_producer,
    };

    HttpServer::new(move || {
        App::new()
            // form size limit 1GB
            .app_data(web::FormConfig::default().limit(1024 * 1024 * 1024))
            //json config limit 10MB
            .app_data(web::JsonConfig::default().limit(10 * 1024 * 1024))
            .app_data(web::Data::new(app_state.clone()))
            .service(
                Files::new("/data", "/data")
                    .show_files_listing()
                    .prefer_utf8(true),
            )
            .service(user::routes())
            .service(status::routes())
            .service(assets::routes().wrap(from_fn(auth_middleware)))
            .service(chat::routes().wrap(from_fn(auth_middleware)))
            .service(game::routes().wrap(from_fn(auth_middleware)))
            .service(proxy::routes().wrap(from_fn(auth_middleware)))
            .wrap(middleware::Logger::default())
            .wrap(middleware::DefaultHeaders::new().add(("X-Version", "0.2")))
            .wrap(
                Cors::default()
                    .allow_any_origin()
                    .allow_any_method()
                    .allow_any_header(),
            )
    })
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}
