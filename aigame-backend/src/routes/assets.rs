// ************************************************************************** //
//                                                                            //
//                                                        :::      ::::::::   //
//   assets.rs                                          :+:      :+:    :+:   //
//                                                    +:+ +:+         +:+     //
//   By: dfine <coding@dfine.tech>                  +#+  +:+       +#+        //
//                                                +#+#+#+#+#+   +#+           //
//   Created: 2025/03/20 20:09:56 by dfine             #+#    #+#             //
//   Updated: 2025/05/05 13:11:53 by dfine            ###   ########.fr       //
//                                                                            //
// ************************************************************************** //

use super::{
    AppState, finder,
    tools::{AudioInfo, ImageInfo, handle_audio, handle_image},
    types::{ErrCode, Error, FileType, GameModule, GenericBody, PptInfo},
};
use crate::{
    db::{
        attachments::{self, Entity as Attachments},
        audios::{self as audio_assets, Entity as AudioAssets},
        images::{self as image_assets, Entity as ImageAssets},
        videos::{self as video_assets, Entity as VideoAssets},
    },
    routes::tools::{VideoInfo, handle_video},
    utils::init::{AUDIO_FORMATS, IMAGE_FORMATS, PPT_FORMATS, VIDEO_FORMATS},
};
use actix_multipart::Multipart;
use actix_web::{
    Responder, Scope, delete, get, post,
    web::{self, Bytes},
};
use anyhow::Result;
use chrono::{DateTime, Utc};
use futures_util::TryStreamExt;
use rabbitmq_stream_client::types::Message;
use sea_orm::{ActiveValue, ColumnTrait, EntityTrait, QueryFilter, QueryOrder, sea_query::Expr};
use serde::{Deserialize, Serialize};
use std::{
    fmt::format,
    path::{Path, PathBuf},
};
use tokio::{
    fs::{File, read_to_string},
    io::AsyncWriteExt,
};
use tracing::*;
use uuid::Uuid;

#[derive(Deserialize)]
struct QueryInfo {
    file_type: String,
    attach_id: Option<i32>,
}
#[derive(Deserialize)]
struct UpdateInfo {
    id: i32,
    status: String,
}

#[derive(Serialize)]
struct MessageObject {
    id: i32,
    path: String,
}
#[derive(Serialize)]
struct GameMessageObject {
    id: i32,
    path: String,
    status: String,
}

#[derive(Serialize, Default)]
struct FileInfo {
    id: i32,
    name: String,

    #[serde(skip_serializing_if = "Option::is_none")]
    url: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    cover: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    width: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    height: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    duration_secs: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    channels: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    sample_rate: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    attach_id: Option<i32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    created_at: Option<DateTime<Utc>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    status: Option<String>,
}

impl FileInfo {
    fn default() -> Self {
        Self {
            name: "undefined".to_string(),
            ..Default::default()
        }
    }
}

#[post("")]
async fn upload(
    app_state: web::Data<AppState>,
    query_info: web::Query<QueryInfo>,
    mut payload: Multipart,
) -> Result<impl Responder, Error> {
    let file_type: FileType = query_info.file_type.as_str().try_into()?;
    let attach_id = query_info.attach_id;
    info!("accept filetype: {}", query_info.file_type.as_str());
    info!("accept attach_id: {:?}", attach_id);
    let mut files_info: Vec<FileInfo> = Vec::new();
    let producer = app_state.parse_producer.clone();
    while let Ok(Some(mut field)) = payload.try_next().await {
        let original_filename = match field.content_disposition().and_then(|cd| cd.get_filename()) {
            Some(name) => name.to_string(),
            None => {
                error!("failed to get filename!");
                return Ok(GenericBody::err(ErrCode::Param));
            }
        };
        let chunked_file_name: String = original_filename.clone().chars().take(100).collect();
        let file_path = Path::new(&original_filename);
        let file_key = Uuid::new_v4().to_string();
        let file_extension = match file_path.extension() {
            Some(ext) => match ext.to_str() {
                Some(ex) => ex,
                None => {
                    error!(
                        "File extension contains invalid UTF-8 characters, filepath: {:?}",
                        file_path
                    );
                    return Ok(GenericBody::err(ErrCode::Param));
                }
            },
            None => {
                error!("failed to unwrap file extension, filepath: {:?}", file_path);
                return Ok(GenericBody::err(ErrCode::Param));
            }
        };
        let savepath = finder::generate_path(file_type.clone(), &file_key, file_extension)
            .await
            .map_err(|e| {
                error!("failed to generate path: {}", e);
                Error::Io
            })?;
        let mut file = File::create(&savepath).await.map_err(|e| {
            error!("failed to create file: {}", e);
            Error::Io
        })?;
        while let Ok(Some(chunk)) = field.try_next().await {
            file.write_all(&chunk).await.map_err(|e| {
                error!("failed to write file: {}", e);
                Error::Io
            })?
        }
        file.sync_all().await.map_err(|e| {
            error!("failed to sync file: {}", e);
            Error::Io
        })?;
        drop(file);
        match file_type {
            FileType::Ppt => {
                if !PPT_FORMATS.contains(&file_extension) {
                    return Ok(GenericBody::err(ErrCode::Type));
                }
                let file_info = attachments::ActiveModel {
                    file_name: ActiveValue::Set(chunked_file_name.to_string()),
                    file_type: ActiveValue::Set(file_type.clone().into()),
                    file_extension: ActiveValue::Set(file_extension.to_string()),
                    file_key: ActiveValue::Set(file_key.clone()),
                    ..Default::default()
                };
                let new_file = Attachments::insert(file_info)
                    .exec(&app_state.db)
                    .await
                    .map_err(|e| {
                        error!("failed to insert attachments to db: {}", e);
                        Error::Db
                    })?;
                files_info.push(FileInfo {
                    id: new_file.last_insert_id,
                    name: original_filename.to_owned(),
                    ..Default::default()
                });
                let message_object = MessageObject {
                    id: new_file.last_insert_id,
                    path: savepath.to_str().unwrap().to_string(),
                };
                let msg = Message::builder()
                    .body(serde_json::to_string(&message_object).unwrap())
                    .build();
                producer
                    .send(msg, |_| async {
                        info!("message sent ");
                    })
                    .await
                    .unwrap();
            }
            FileType::Image => {
                if query_info.attach_id.is_none() {
                    return Ok(GenericBody::err(ErrCode::Param));
                }
                if !IMAGE_FORMATS.contains(&file_extension) {
                    return Ok(GenericBody::err(ErrCode::Type));
                }
                let image_info: ImageInfo = handle_image(savepath.to_str().unwrap())?;
                let file_info = image_assets::ActiveModel {
                    tag: ActiveValue::Set(Some(chunked_file_name.to_string())),
                    ori_width: ActiveValue::Set(image_info.width),
                    ori_height: ActiveValue::Set(image_info.height),
                    attach_id: ActiveValue::Set(attach_id.unwrap()),
                    file_extension: ActiveValue::Set(file_extension.to_string()),
                    file_key: ActiveValue::Set(file_key.clone()),
                    ..Default::default()
                };
                let new_file = ImageAssets::insert(file_info)
                    .exec(&app_state.db)
                    .await
                    .map_err(|e| {
                        error!("failed to insert image to db: {}", e);
                        Error::Db
                    })?;
                files_info.push(FileInfo {
                    id: new_file.last_insert_id,
                    name: original_filename.to_owned(),
                    width: Some(image_info.width),
                    height: Some(image_info.height),
                    attach_id: attach_id,
                    url: {
                        let url =
                            match finder::find_url(file_type.clone(), &file_key, file_extension) {
                                Ok(path) => path,
                                Err(e) => {
                                    error!("failed to find path: {}", e);
                                    String::new()
                                }
                            };
                        Some(url)
                    },
                    ..Default::default()
                });
            }
            FileType::Audio => {
                if query_info.attach_id.is_none() {
                    return Ok(GenericBody::err(ErrCode::Param));
                }
                if !AUDIO_FORMATS.contains(&file_extension) {
                    return Ok(GenericBody::err(ErrCode::Type));
                }
                let audio_info: AudioInfo = handle_audio(savepath.to_str().unwrap())?;
                let file_info = audio_assets::ActiveModel {
                    tag: ActiveValue::Set(Some(chunked_file_name.to_string())),
                    duration_secs: ActiveValue::Set(audio_info.duration_secs),
                    sample_rate: ActiveValue::Set(audio_info.sample_rate),
                    channels: ActiveValue::Set(audio_info.channels as u32),
                    attach_id: ActiveValue::Set(attach_id.unwrap()),
                    file_extension: ActiveValue::Set(file_extension.to_string()),
                    file_key: ActiveValue::Set(file_key.clone()),
                    ..Default::default()
                };
                let new_file = AudioAssets::insert(file_info)
                    .exec(&app_state.db)
                    .await
                    .map_err(|e| {
                        error!("failed to insert audio to db: {}", e);
                        Error::Db
                    })?;
                files_info.push(FileInfo {
                    id: new_file.last_insert_id,
                    name: original_filename.to_owned(),
                    duration_secs: Some(audio_info.duration_secs),
                    channels: Some(audio_info.channels as u32),
                    sample_rate: Some(audio_info.sample_rate),
                    attach_id: attach_id,
                    url: {
                        let url =
                            match finder::find_url(file_type.clone(), &file_key, file_extension) {
                                Ok(path) => path,
                                Err(e) => {
                                    error!("failed to find path: {}", e);
                                    String::new()
                                }
                            };
                        Some(url)
                    },
                    ..Default::default()
                });
            }
            FileType::Video => {
                if query_info.attach_id.is_none() {
                    return Ok(GenericBody::err(ErrCode::Param));
                }
                if !VIDEO_FORMATS.contains(&file_extension) {
                    return Ok(GenericBody::err(ErrCode::Type));
                }
                let video_info: VideoInfo = handle_video(savepath.to_str().unwrap())?;
                let file_info = video_assets::ActiveModel {
                    tag: ActiveValue::Set(Some(chunked_file_name.to_string())),
                    duration_secs: ActiveValue::Set(video_info.duration_secs),
                    ori_width: ActiveValue::Set(video_info.width),
                    ori_height: ActiveValue::Set(video_info.height),
                    attach_id: ActiveValue::Set(attach_id.unwrap()),
                    file_extension: ActiveValue::Set(file_extension.to_string()),
                    file_key: ActiveValue::Set(file_key.clone()),
                    ..Default::default()
                };
                let new_file = VideoAssets::insert(file_info)
                    .exec(&app_state.db)
                    .await
                    .map_err(|e| {
                        error!("failed to insert video to db: {}", e);
                        Error::Db
                    })?;
                files_info.push(FileInfo {
                    id: new_file.last_insert_id,
                    name: original_filename.to_owned(),
                    width: Some(video_info.width),
                    height: Some(video_info.height),
                    duration_secs: Some(video_info.duration_secs),
                    attach_id: attach_id,
                    url: {
                        let url =
                            match finder::find_url(file_type.clone(), &file_key, file_extension) {
                                Ok(path) => path,
                                Err(e) => {
                                    error!("failed to find path: {}", e);
                                    String::new()
                                }
                            };
                        Some(url)
                    },
                    ..Default::default()
                });
            }
            _ => return Err(Error::Type),
        }
    }
    Ok(GenericBody::<Vec<FileInfo>>::new(
        "File uploaded successfully.",
        Some(files_info),
    ))
}

#[get("")]
async fn query(
    app_state: web::Data<AppState>,
    query_info: web::Query<QueryInfo>,
) -> Result<impl Responder, Error> {
    let file_type: FileType = query_info.file_type.as_str().try_into()?;
    let attach_id = query_info.attach_id;

    let files_info: Vec<FileInfo> = match file_type {
        FileType::Ppt => {
            let mut query_filter = Attachments::find().filter(attachments::Column::Valid.eq(true));
            if let Some(attach_id) = attach_id {
                query_filter = query_filter.filter(attachments::Column::Id.eq(attach_id));
            }
            query_filter
                .order_by_desc(attachments::Column::CreatedAt)
                .all(&app_state.db)
                .await
                .map_err(|_| Error::Db)?
                .iter()
                .map(|attach| FileInfo {
                    id: attach.id,
                    name: attach.file_name.clone(),
                    status: Some(attach.status.clone()),
                    created_at: attach.created_at,
                    cover: attach.cover.clone(),
                    ..FileInfo::default()
                })
                .collect()
        }
        FileType::Image => {
            let mut query_filter = ImageAssets::find().filter(image_assets::Column::Valid.eq(true));
            if let Some(attach_id) = attach_id {
                query_filter = query_filter.filter(image_assets::Column::AttachId.eq(attach_id));
            }

            query_filter
                .all(&app_state.db)
                .await
                .map_err(|_| Error::Db)?
                .iter()
                .map(|attach| FileInfo {
                    id: attach.id,
                    name: attach.tag.clone().unwrap(),
                    url: {
                        let url = match finder::find_url(
                            file_type.clone(),
                            &attach.file_key,
                            &attach.file_extension,
                        ) {
                            Ok(path) => path,
                            Err(e) => {
                                error!("failed to find path: {}", e);
                                String::new()
                            }
                        };
                        Some(url)
                    },
                    width: Some(attach.ori_width),
                    height: Some(attach.ori_height),
                    attach_id: Some(attach.attach_id),
                    created_at: attach.created_at,
                    ..FileInfo::default()
                })
                .collect()
        }

        FileType::Audio => {
            let mut query_filter = AudioAssets::find().filter(audio_assets::Column::Valid.eq(true));
            if let Some(attach_id) = attach_id {
                query_filter = query_filter.filter(audio_assets::Column::AttachId.eq(attach_id));
            }
            query_filter
                .all(&app_state.db)
                .await
                .map_err(|_| Error::Db)?
                .iter()
                .map(|attach| FileInfo {
                    id: attach.id,
                    name: attach.tag.clone().unwrap(),
                    url: {
                        let url = match finder::find_url(
                            file_type.clone(),
                            &attach.file_key,
                            &attach.file_extension,
                        ) {
                            Ok(path) => path,
                            Err(e) => {
                                error!("failed to find path: {}", e);
                                String::new()
                            }
                        };
                        Some(url)
                    },
                    duration_secs: Some(attach.duration_secs),
                    channels: Some(attach.channels),
                    sample_rate: Some(attach.sample_rate),
                    attach_id: Some(attach.attach_id),
                    created_at: attach.created_at,
                    ..FileInfo::default()
                })
                .collect()
        }
        FileType::Video => {
            let mut query_filter = VideoAssets::find().filter(video_assets::Column::Valid.eq(true));
            if let Some(attach_id) = attach_id {
                query_filter = query_filter.filter(video_assets::Column::AttachId.eq(attach_id));
            }
            query_filter
                .all(&app_state.db)
                .await
                .map_err(|_| Error::Db)?
                .iter()
                .map(|attach| FileInfo {
                    id: attach.id,
                    name: attach.tag.clone().unwrap(),
                    url: {
                        let url = match finder::find_url(
                            file_type.clone(),
                            &attach.file_key,
                            &attach.file_extension,
                        ) {
                            Ok(path) => path,
                            Err(e) => {
                                error!("failed to find path: {}", e);
                                String::new()
                            }
                        };
                        Some(url)
                    },
                    duration_secs: Some(attach.duration_secs),
                    attach_id: Some(attach.attach_id),
                    width: Some(attach.ori_width),
                    height: Some(attach.ori_height),
                    created_at: attach.created_at,
                    ..FileInfo::default()
                })
                .collect()
        }
        _ => return Err(Error::Type),
    };

    Ok(GenericBody::<Vec<FileInfo>>::new(
        "Files found successfully.",
        Some(files_info),
    ))
}

#[derive(Deserialize)]
struct DeleteInfo {
    file_type: String,
    id: i32,
}

#[delete("")]
async fn delete(
    app_state: web::Data<AppState>,
    delete_info: web::Query<DeleteInfo>,
) -> Result<impl Responder, Error> {
    let file_type: FileType = delete_info.file_type.as_str().try_into()?;

    match file_type {
        FileType::Ppt => Attachments::update_many()
            .col_expr(attachments::Column::Valid, Expr::value(false))
            .filter(attachments::Column::Id.eq(delete_info.id))
            .exec(&app_state.db)
            .await
            .map_err(|e| {
                error!("failed to update db status: {}", e);
                Error::Db
            })?,
        FileType::Image => ImageAssets::update_many()
            .col_expr(attachments::Column::Valid, Expr::value(false))
            .filter(attachments::Column::Id.eq(delete_info.id))
            .exec(&app_state.db)
            .await
            .map_err(|e| {
                error!("failed to update db status: {}", e);
                Error::Db
            })?,
        FileType::Audio => AudioAssets::update_many()
            .col_expr(attachments::Column::Valid, Expr::value(false))
            .filter(attachments::Column::Id.eq(delete_info.id))
            .exec(&app_state.db)
            .await
            .map_err(|e| {
                error!("failed to update db status: {}", e);
                Error::Db
            })?,
        _ => return Err(Error::Type),
    };

    Ok(GenericBody::<Vec<FileInfo>>::new(
        "File deleted successfully.",
        None,
    ))
}

#[post("/update_status")]
async fn update_status(
    app_state: web::Data<AppState>,
    update_info: web::Json<UpdateInfo>,
) -> impl Responder {
    let attach = Attachments::find_by_id(update_info.id)
        .one(&app_state.db)
        .await;
    let some_attach = match attach {
        Ok(Some(some_attach)) => some_attach,
        Ok(None) => {
            warn!("id:{} not exist in db!", update_info.id);
            return GenericBody::err(ErrCode::DataBase);
        }

        Err(e) => {
            error!("query db error: {}", e);
            return GenericBody::err(ErrCode::DataBase);
        }
    };

    if update_info.status != "parse" {
        let update_result = Attachments::update_many()
            .col_expr(
                attachments::Column::Status,
                Expr::value(update_info.status.to_owned()),
            )
            .filter(attachments::Column::Id.eq(update_info.id))
            .exec(&app_state.db)
            .await;
        if update_result.is_err() {
            error!("update db error: {:?}", update_result.as_ref().err());
            return GenericBody::err(ErrCode::DataBase);
        }
        return GenericBody::<Vec<FileInfo>>::new("status updated", None);
    }

    let attach_config = match finder::find_module(some_attach.file_key.as_ref(), GameModule::Parse)
    {
        Ok(attach_config) => attach_config,
        Err(e) => {
            error!("failed to find attach config path: {}", e);
            return GenericBody::err(ErrCode::DataBase);
        }
    };
    let attach_parse_config: PptInfo = match PptInfo::read(attach_config).await {
        Ok(att) => att,
        Err(e) => {
            error!("failed to read attach config: {}", e);
            return GenericBody::err(ErrCode::Param);
        }
    };
    if attach_parse_config
        .insert_data(&app_state.db, update_info.id)
        .await
        .is_err()
    {
        error!("failed to insert data");
        return GenericBody::err(ErrCode::DataBase);
    };

    let cover = match finder::screenshot(some_attach.file_key.as_ref()) {
        Some(screenshots) => screenshots.first().cloned(),
        None => None,
    };
    let update_result = Attachments::update_many()
        .col_expr(
            attachments::Column::Status,
            Expr::value(update_info.status.to_owned()),
        )
        .col_expr(attachments::Column::Cover, Expr::value(cover))
        .filter(attachments::Column::Id.eq(update_info.id))
        .exec(&app_state.db)
        .await;
    if update_result.is_err() {
        error!("update db error: {:?}", update_result.as_ref().err());
        return GenericBody::err(ErrCode::DataBase);
    }
    GenericBody::<Vec<FileInfo>>::new("status updated", None)
}

#[derive(Deserialize)]
struct QueryImageParam {
    attach_id: i32,
}

#[get("/screenshot")]
async fn screenshot(
    app_state: web::Data<AppState>,
    param: web::Query<QueryImageParam>,
) -> impl Responder {
    let attach = Attachments::find_by_id(param.attach_id)
        .one(&app_state.db)
        .await;
    let some_attach = match attach {
        Ok(some_attach) => some_attach,
        Err(e) => {
            error!("query db error: {}", e);
            return GenericBody::err(ErrCode::DataBase);
        }
    };
    if some_attach.is_none() {
        warn!("id:{} not exist in db!", param.attach_id);
        return GenericBody::err(ErrCode::DataBase);
    }
    let files = finder::screenshot(&some_attach.unwrap().file_key);
    GenericBody::new("screenshot query finished.", files)
}

#[derive(Deserialize)]
struct QueryAttchParam {
    id: i32,
    module_type: String,
}

#[get("/module")]
async fn module(
    app_state: web::Data<AppState>,
    query_info: web::Query<QueryAttchParam>,
) -> Result<impl Responder, Error> {
    let module_type: GameModule = query_info.module_type.as_str().into();
    let file_path = match module_type {
        GameModule::Parse => {
            let attach = Attachments::find_by_id(query_info.id)
                .one(&app_state.db)
                .await
                .map_err(|e| {
                    error!("query db error: {}", e);
                    Error::Db
                })?;
            if attach.is_none() {
                warn!("id:{} not exist in db!", query_info.id);
                return Ok(GenericBody::err(ErrCode::DataBase));
            }
            finder::find_module(
                attach.unwrap().file_key.clone().as_str(),
                module_type.clone(),
            )
            .map_err(|e| {
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
    let json: serde_json::Value = serde_json::from_str(&module_data).map_err(|e| {
        error!("failed to serialize json: {}", e);
        Error::Format
    })?;

    Ok(GenericBody::new("query module json finished", Some(json)))
}

#[post("/module")]
async fn handle_module(
    app_state: web::Data<AppState>,
    query_info: web::Query<QueryAttchParam>,
    raw_body: Bytes,
) -> Result<impl Responder, Error> {
    info!("Received POST request to /module");
    let module_type: GameModule = query_info.module_type.as_str().into();
    let file_path = match module_type {
        GameModule::Parse => {
            let attach = Attachments::find_by_id(query_info.id)
                .one(&app_state.db)
                .await
                .map_err(|e| {
                    error!("query db error: {}", e);
                    Error::Db
                })?;
            if attach.is_none() {
                warn!("id:{} not exist in db!", query_info.id);
                return Ok(GenericBody::<i32>::err(ErrCode::DataBase));
            }
            finder::find_module(
                attach.unwrap().file_key.clone().as_str(),
                module_type.clone(),
            )
            .map_err(|e| {
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

#[get("/process")]
async fn ppt_process(
    app_state: web::Data<AppState>,
    query_info: web::Query<QueryImageParam>,
) -> Result<impl Responder, Error> {
    let attach = match Attachments::find_by_id(query_info.attach_id)
        .one(&app_state.db)
        .await
        .map_err(|e| {
            error!("query db error: {}", e);
            Error::Db
        })? {
        Some(attach) => attach,
        _ => {
            warn!("id:{} not exist in db!", query_info.attach_id);
            return Ok(GenericBody::err(ErrCode::DataBase));
        }
    };
    let ppt_path =
        match finder::generate_path(FileType::Ppt, attach.file_key.as_ref(), "pptx").await {
            Ok(p) => p.to_str().unwrap().to_string(),
            Err(e) => {
                error!(
                    "failed to find ppt path, id: {}, error:{}",
                    query_info.attach_id, e
                );
                return Ok(GenericBody::err(ErrCode::UnKnown));
            }
        };
    let message_object = MessageObject {
        id: attach.id,
        path: ppt_path,
    };

    let msg = Message::builder()
        .body(serde_json::to_string(&message_object).unwrap())
        .build();
    let producer = app_state.parse_producer.clone();
    producer
        .send(msg, |_| async {
            info!("message sent ");
        })
        .await
        .unwrap();
    Ok(GenericBody::<i32>::new("ppt process message sent", None))
}

pub fn routes() -> Scope {
    web::scope("/attach")
        .service(upload)
        .service(query)
        .service(update_status)
        .service(screenshot)
        .service(module)
        .service(handle_module)
        .service(ppt_process)
        .service(delete)
    //.service(generate)
}
