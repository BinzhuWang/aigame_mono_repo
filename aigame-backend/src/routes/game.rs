// ************************************************************************** //
//                                                                            //
//                                                        :::      ::::::::   //
//   game.rs                                            :+:      :+:    :+:   //
//                                                    +:+ +:+         +:+     //
//   By: dfine <coding@dfine.tech>                  +#+  +:+       +#+        //
//                                                +#+#+#+#+#+   +#+           //
//   Created: 2025/04/15 17:04:05 by dfine             #+#    #+#             //
//   Updated: 2025/04/23 13:56:09 by dfine            ###   ########.fr       //
//                                                                            //
// ************************************************************************** //

use super::{
    AppState, finder,
    types::{ErrCode, Error, GameModule, GenericBody},
};
use crate::db::gamecases::{self, Entity as GameCases};
use actix_web::{
    Responder, Scope, delete, get, post,
    web::{self, Bytes},
};
use rabbitmq_stream_client::types::Message;
use sea_orm::{
    ActiveModelTrait, ActiveValue, ColumnTrait, Condition, EntityTrait, QueryFilter,
    sea_query::Expr,
};
use serde::{Deserialize, Serialize};
use tokio::{
    fs::{File, read_to_string},
    io::AsyncWriteExt,
};
use tracing::*;

#[derive(Deserialize)]
struct GameInfo {
    attach_id: i32,
    status: String,
    module_id: i32,
    file_key: String,
}

#[post("/create")]
async fn create(
    app_state: web::Data<AppState>,
    params: web::Json<GameInfo>,
) -> Result<impl Responder, Error> {
    info!(
        "create gamecase: accept attach_id: {}, file_key:{}",
        params.attach_id,
        params.file_key.clone()
    );
    let game_info = gamecases::ActiveModel {
        attach_id: ActiveValue::Set(params.attach_id),
        status: ActiveValue::Set(params.status.clone()),
        file_key: ActiveValue::Set(params.file_key.clone()),
        module_id: ActiveValue::Set(params.module_id),
        ..Default::default()
    };
    let new_game = GameCases::insert(game_info)
        .exec(&app_state.db)
        .await
        .map_err(|e| {
            error!("failed to insert attachments to db: {}", e);
            Error::Db
        })?;
    Ok(GenericBody::<i32>::new(
        "create game case successfully",
        Some(new_game.last_insert_id),
    ))
}

#[derive(Deserialize)]
struct GenerateParam {
    id: i32,
}

#[derive(Serialize)]
struct MessageObject {
    id: i32,
    file_key: String,
    module_id: i32,
    status: String,
}

#[post("/generate")]
async fn generate(
    app_state: web::Data<AppState>,
    params: web::Json<GenerateParam>,
) -> Result<impl Responder, Error> {
    let game = match GameCases::find_by_id(params.id)
        .one(&app_state.db)
        .await
        .map_err(|_| Error::Db)?
    {
        Some(game) => game,
        _ => {
            error!("invalid game id");
            return Ok(GenericBody::err(ErrCode::DataBase));
        }
    };

    let message_object = MessageObject {
        id: game.id,
        file_key: game.file_key.clone(),
        module_id: game.module_id,
        status: game.status.clone(),
    };
    let producer = app_state.game_producer.clone();
    let msg = Message::builder()
        .body(serde_json::to_string(&message_object).unwrap())
        .build();
    producer
        .send(msg, |_| async {
            info!("game generate message sent ");
        })
        .await
        .unwrap();
    Ok(GenericBody::<Vec<GameModel>>::new(
        "game generate message has been sent",
        None,
    ))
}

#[get("/regen/{id}/{status}")]
async fn regenerate(
    app_state: web::Data<AppState>,
    path: web::Path<(i32, String)>,
) -> Result<impl Responder, Error> {
    let (id, status) = path.into_inner();
    let parent_status = match status.as_str() {
        "code" => "plan",
        _ => "goal",
    };
    let game = gamecases::ActiveModel {
        id: ActiveValue::Set(id),
        status: ActiveValue::Set(parent_status.to_string()),
        ..Default::default()
    };
    let update_case = game.update(&app_state.db).await.map_err(|e| {
        error!("failed to update game status: {}", e);
        Error::Db
    })?;

    let message_object = MessageObject {
        id,
        file_key: update_case.file_key.clone(),
        module_id: update_case.module_id,
        status: update_case.status.clone(),
    };
    let producer = app_state.game_producer.clone();
    let msg = Message::builder()
        .body(serde_json::to_string(&message_object).unwrap())
        .build();
    producer
        .send(msg, |_| async {
            info!("game generate message sent ");
        })
        .await
        .unwrap();

    Ok(GenericBody::<Vec<GameModel>>::new(
        "game regenerating message has been sent",
        None,
    ))
}

#[derive(Serialize)]
struct GameModel {
    id: i32,
    status: String,
    attach_id: i32,
    module_id: i32,
    access_url: Option<String>,
}

#[derive(Deserialize)]
struct QueryParam {
    id: Option<i32>,
    attach_id: Option<i32>,
}

#[get("/query")]
async fn query(
    app_state: web::Data<AppState>,
    query_param: web::Query<QueryParam>,
) -> Result<impl Responder, Error> {
    let mut filter_condition = Condition::all();
    if let Some(id) = query_param.id {
        filter_condition = filter_condition.add(gamecases::Column::Id.eq(id));
    }
    if let Some(attach_id) = query_param.attach_id {
        filter_condition = filter_condition.add(gamecases::Column::AttachId.eq(attach_id));
    }
    let game_info: Vec<GameModel> = GameCases::find()
        .filter(gamecases::Column::Valid.eq(true))
        .filter(filter_condition)
        .all(&app_state.db)
        .await
        .map_err(|_| Error::Db)?
        .iter()
        .map(|game| GameModel {
            id: game.id,
            status: game.status.clone(),
            attach_id: game.attach_id,
            module_id: game.module_id,
            access_url: game.access_url.clone(),
        })
        .collect();
    Ok(GenericBody::<Vec<GameModel>>::new(
        "game query successfully",
        Some(game_info),
    ))
}

#[derive(Deserialize)]
struct UpdateInfo {
    id: i32,
    status: String,
    #[serde(default)]
    access_url: Option<String>,
}

#[derive(Deserialize)]
struct QueryGameParam {
    id: i32,
    module_type: String,
}
#[get("/module")]
async fn module(
    app_state: web::Data<AppState>,
    query_info: web::Query<QueryGameParam>,
) -> Result<impl Responder, Error> {
    let module_type: GameModule = query_info.module_type.as_str().into();
    let file_path = match module_type {
        GameModule::Plan | GameModule::Goal | GameModule::Code => {
            let game = GameCases::find_by_id(query_info.id)
                .one(&app_state.db)
                .await
                .map_err(|e| {
                    error!("query db error: {}", e);
                    Error::Db
                })?;
            if game.is_none() {
                warn!("id:{} not exist in db!", query_info.id);
                return Ok(GenericBody::err(ErrCode::DataBase));
            }
            finder::find_module(&game.unwrap().file_key, module_type.clone()).map_err(|e| {
                error!("failed to get file path, {}", e);
                Error::Io
            })?
        }
        _ => {
            return Ok(GenericBody::err(ErrCode::Param));
        }
    };
    info!("module path: {}", file_path.to_str().unwrap());
    let module_data = read_to_string(file_path).await.map_err(|e| {
        error!("failed to read file, {}", e);
        Error::Io
    })?;
    match module_type {
        GameModule::Code => {
            // App.tsx 是代码文本，直接包装为字符串
            Ok(GenericBody::new(
                "query module code finished",
                Some(serde_json::json!({ "code": module_data })),
            ))
        }
        _ => {
            // 其他模块为 JSON 内容，尝试解析
            let json: serde_json::Value = serde_json::from_str(&module_data).map_err(|e| {
                error!("failed to serialize json: {}", e);
                Error::Format
            })?;
            Ok(GenericBody::new("query module json finished", Some(json)))
        }
    }
}

#[post("/module")]
async fn handle_module(
    app_state: web::Data<AppState>,
    query_info: web::Query<QueryGameParam>,
    raw_body: Bytes,
) -> Result<impl Responder, Error> {
    info!("Received POST request to /module");
    let module_type: GameModule = query_info.module_type.as_str().into();
    let file_path = match module_type {
        GameModule::Plan | GameModule::Goal | GameModule::Code => {
            let game = GameCases::find_by_id(query_info.id)
                .one(&app_state.db)
                .await
                .map_err(|e| {
                    error!("query db error: {}", e);
                    Error::Db
                })?;
            if game.is_none() {
                warn!("id:{} not exist in db!", query_info.id);
                return Ok(GenericBody::<i32>::err(ErrCode::DataBase));
            }
            finder::find_module(&game.unwrap().file_key, module_type.clone()).map_err(|e| {
                error!("failed to get file path, {}", e);
                Error::Io
            })?
        }
        _ => {
            return Ok(GenericBody::err(ErrCode::Param));
        }
    };
    info!("module path: {}", file_path.to_str().unwrap());

    let mut file = File::create(&file_path).await.map_err(|e| {
        error!(
            "failed to create file: {}, error: {}",
            &file_path.to_str().unwrap(),
            e
        );
        Error::Io
    })?;

    file.write_all(&raw_body).await.map_err(|e| {
        error!(
            "failed to create file: {}, error: {}",
            &file_path.to_str().unwrap(),
            e
        );
        Error::Io
    })?;
    info!("write raw body finished: {}", &file_path.to_str().unwrap());
    _ = file.flush().await;
    Ok(GenericBody::new("modify module json finished", None))
}

#[post("/update_status")]
async fn update_status(
    app_state: web::Data<AppState>,
    update_info: web::Json<UpdateInfo>,
) -> Result<impl Responder, Error> {
    let game = GameCases::find_by_id(update_info.id)
        .one(&app_state.db)
        .await
        .map_err(|_| Error::Db)?;

    if game.is_none() {
        error!("invalid game id");
        return Ok(GenericBody::err(ErrCode::DataBase));
    }
    let mut updater = GameCases::update_many().col_expr(
        gamecases::Column::Status,
        Expr::value(update_info.status.to_owned()),
    );
    if update_info.access_url.is_some() {
        updater = updater.col_expr(
            gamecases::Column::AccessUrl,
            Expr::value(update_info.access_url.to_owned()),
        )
    }
    let _result = updater
        .filter(gamecases::Column::Id.eq(update_info.id))
        .exec(&app_state.db)
        .await
        .map_err(|e| {
            error!("failed to update game status: {}", e);
            Error::Db
        });
    Ok(GenericBody::<Vec<GameModel>>::new(
        "game status update successfully",
        None,
    ))
}

#[delete("")]
async fn delete(
    app_state: web::Data<AppState>,
    query_param: web::Query<QueryParam>,
) -> Result<impl Responder, Error> {
    let mut filter_condition = Condition::all();
    if let Some(id) = query_param.id {
        filter_condition = filter_condition.add(gamecases::Column::Id.eq(id));
    }
    if let Some(attach_id) = query_param.attach_id {
        filter_condition = filter_condition.add(gamecases::Column::AttachId.eq(attach_id));
    }
    GameCases::update_many()
        .col_expr(gamecases::Column::Valid, Expr::value(false))
        .filter(filter_condition)
        .filter(gamecases::Column::Valid.eq(true))
        .exec(&app_state.db)
        .await
        .map_err(|e| {
            error!("failed to update db status: {}", e);
            Error::Db
        })?;
    Ok(GenericBody::<i32>::new("Game deleted successfully.", None))
}

pub fn routes() -> Scope {
    web::scope("/game")
        .service(create)
        .service(query)
        .service(generate)
        .service(regenerate)
        .service(delete)
        .service(update_status)
        .service(module)
        .service(handle_module)
}
