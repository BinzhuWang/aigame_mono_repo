// ************************************************************************** //
//                                                                            //
//                                                        :::      ::::::::   //
//   types.rs                                           :+:      :+:    :+:   //
//                                                    +:+ +:+         +:+     //
//   By: dfine <coding@dfine.tech>                  +#+  +:+       +#+        //
//                                                +#+#+#+#+#+   +#+           //
//   Created: 2025/03/21 16:08:22 by dfine             #+#    #+#             //
//   Updated: 2025/04/15 17:04:22 by dfine            ###   ########.fr       //
//                                                                            //
// ************************************************************************** //

use std::path::PathBuf;

use crate::db::{
    audios::{self, Entity as Audios},
    images::{self, Entity as Images},
};
use actix_web::{
    HttpRequest, HttpResponse, Responder, ResponseError,
    body::BoxBody,
    http::{StatusCode, header::ContentType},
};
use sea_orm::{ActiveValue, DatabaseConnection, EntityTrait};
use serde::{Deserialize, Serialize};
use tracing::error;
#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("failed to read/write file.")]
    Io,
    #[error("invalid file type.")]
    Type,
    #[error("query/insert database error.")]
    Db,
    #[error("file format error.")]
    Format,
    #[error("network error.")]
    Network,
}

impl ResponseError for Error {
    fn status_code(&self) -> StatusCode {
        match &self {
            Error::Type => StatusCode::UNSUPPORTED_MEDIA_TYPE,
            _ => StatusCode::INTERNAL_SERVER_ERROR,
        }
    }
    fn error_response(&self) -> HttpResponse {
        HttpResponse::build(self.status_code()).body(self.to_string())
    }
}

#[derive(Clone)]
pub enum GameModule {
    Parse,
    Goal,
    Design,
    Plan,
    Asset,
    Code,
    Unknown,
}

impl From<&str> for GameModule {
    fn from(m: &str) -> Self {
        match m {
            "parse" => Self::Parse,
            "goal" => Self::Goal,
            "design" => Self::Design,
            "plan" => Self::Plan,
            "asset" => Self::Asset,
            "code" => Self::Code,
            _ => Self::Unknown,
        }
    }
}

impl GameModule {
    pub fn filename(&self) -> Option<String> {
        match self {
            Self::Parse => Some("parse.json".to_string()),
            Self::Goal => Some("goal.json".to_string()),
            Self::Design => Some("design.json".to_string()),
            Self::Plan => Some("plan.json".to_string()),
            Self::Asset => Some("asset.json".to_string()),
            Self::Code => Some("App.tsx".to_string()),
            _ => None,
        }
    }
}

pub enum ErrCode {
    Type,
    DataBase,
    Param,
    Custom(String),
    UnKnown,
}
impl ErrCode {
    pub fn info(&self) -> (u16, String) {
        match self {
            Self::Type => (400, "Unsupported Media Type".to_string()),
            Self::DataBase => (50040, "Database Error".to_string()),
            Self::Param => (40001, "Invalid Parameter".to_string()),
            Self::Custom(msg) => (40002, msg.to_owned()),
            _ => (599, "Don't panic, C'est la vie".to_string()),
        }
    }
}

#[derive(Clone)]
pub enum FileType {
    Ppt,
    Image,
    Audio,
    Video,
    Chat,
}

impl TryFrom<&str> for FileType {
    type Error = Error;
    fn try_from(file_type: &str) -> Result<Self, Self::Error> {
        match file_type {
            "ppt" => Ok(Self::Ppt),
            "audio" => Ok(Self::Audio),
            "video" => Ok(Self::Video),
            "image" => Ok(Self::Image),
            _ => Err(Error::Type),
        }
    }
}

impl From<FileType> for String {
    fn from(file_type: FileType) -> String {
        match file_type {
            FileType::Ppt => "ppt".to_string(),
            FileType::Audio => "audio".to_string(),
            FileType::Video => "video".to_string(),
            FileType::Image => "image".to_string(),
            FileType::Chat => "chat".to_string(),
        }
    }
}

#[derive(Debug, Serialize)]
pub struct GenericBody<T: Serialize> {
    code: u16,
    msg: String,
    result: Option<T>,
}

impl<T> GenericBody<T>
where
    T: Serialize,
{
    pub fn new(msg: impl Into<String>, result: Option<T>) -> Self {
        Self {
            code: 200,
            msg: msg.into(),
            result,
        }
    }
    pub fn err(err: ErrCode) -> Self {
        let (code, msg) = err.info();
        Self {
            code,
            msg,
            result: None,
        }
    }
}

impl<T> Responder for GenericBody<T>
where
    T: Serialize,
{
    type Body = BoxBody;
    fn respond_to(self, _req: &HttpRequest) -> HttpResponse<Self::Body> {
        let body = serde_json::to_string(&self).unwrap();
        HttpResponse::Ok()
            .content_type(ContentType::json())
            .body(body)
    }
}

#[derive(Debug, Deserialize, Clone)]
pub struct PptInfo {
    document_info: Vec<SlideInfo>,
    pdf_url: Option<String>,
}

#[derive(Debug, Deserialize, Clone)]
struct SlideInfo {
    page: u32,
    title: Option<String>,
    text: Vec<String>,
    images: Vec<ImageInfo>,
    videos: Vec<VideoInfo>,
    audios: Vec<AudioInfo>,
    notes: Option<String>,
    module_id: Option<i32>,
    screenshot: String,
}

#[derive(Debug, Deserialize, Clone)]
struct VideoInfo {
    path: String,
    left: f64,
    top: f64,
    width: f64,
    height: f64,
    tag: Option<String>,
    desp: Option<String>,
}

#[derive(Debug, Deserialize, Clone)]
struct ImageInfo {
    path: String,
    left: f32,
    top: f32,
    width: f32,
    height: f32,
    tag: Option<String>,
    desp: Option<String>,
    ori_width: u32,
    ori_height: u32,
}

#[derive(Debug, Deserialize, Clone)]
struct AudioInfo {
    path: String,
    left: f32,
    top: f32,
    width: f32,
    height: f32,
    tag: Option<String>,
    desp: Option<String>,
    sample_rate: u32,
    duration_secs: f32,
    channels: u32,
}

impl PptInfo {
    pub async fn read(path: PathBuf) -> Result<PptInfo, Error> {
        let data = tokio::fs::read_to_string(path).await.map_err(|e| {
            error!("failed to read file: {}", e);
            Error::Io
        })?;

        let parsed_data: PptInfo = serde_json::from_str(&data).map_err(|e| {
            error!("failed to parse file: {}", e);
            Error::Format
        })?;
        Ok(parsed_data)
    }
    pub async fn insert_data(&self, db: &DatabaseConnection, attach_id: i32) -> Result<(), Error> {
        for slide in self.document_info.clone() {
            let image_info: Vec<ImageInfo> = slide.images;
            let audio_info: Vec<AudioInfo> = slide.audios;
            Self::insert_images(db, image_info, slide.page, attach_id).await?;
            Self::insert_audios(db, audio_info, slide.page, attach_id).await?;
        }
        Ok(())
    }

    async fn insert_images(
        db: &DatabaseConnection,
        image_info: Vec<ImageInfo>,
        page: u32,
        attach_id: i32,
    ) -> Result<(), Error> {
        if image_info.is_empty() {
            return Ok(());
        }
        let image_records: Vec<images::ActiveModel> = image_info
            .iter()
            .map(|img| {
                println!("file_key:{}", img.path.clone());
                images::ActiveModel {
                    tag: ActiveValue::Set(img.tag.as_ref().map(|s| s.chars().take(32).collect())),
                    file_key: ActiveValue::Set(img.path.clone()),
                    top: ActiveValue::Set(img.top),
                    left: ActiveValue::Set(img.left),
                    width: ActiveValue::Set(img.width),
                    height: ActiveValue::Set(img.height),
                    ori_width: ActiveValue::Set(img.ori_width),
                    ori_height: ActiveValue::Set(img.ori_height),
                    attach_id: ActiveValue::Set(attach_id),
                    page: ActiveValue::Set(page),
                    source_type: ActiveValue::Set("ppt_parse".to_string()),
                    desp: ActiveValue::Set(
                        img.desp.as_ref().map(|s| s.chars().take(512).collect()),
                    ),
                    ..Default::default()
                }
            })
            .collect();
        let _ = Images::insert_many(image_records)
            .exec(db)
            .await
            .map_err(|e| {
                error!("failed to insert images, {}", e);
                Error::Db
            });
        Ok(())
    }
    async fn insert_audios(
        db: &DatabaseConnection,
        audio_info: Vec<AudioInfo>,
        page: u32,
        attach_id: i32,
    ) -> Result<(), Error> {
        if audio_info.is_empty() {
            return Ok(());
        }
        let audio_records: Vec<audios::ActiveModel> = audio_info
            .iter()
            .map(|aud| audios::ActiveModel {
                tag: ActiveValue::Set(aud.tag.as_ref().map(|s| s.chars().take(32).collect())),
                file_key: ActiveValue::Set(aud.path.clone()),
                attach_id: ActiveValue::Set(attach_id),
                page: ActiveValue::Set(page),
                source_type: ActiveValue::Set("ppt_parse".to_string()),
                sample_rate: ActiveValue::Set(aud.sample_rate),
                duration_secs: ActiveValue::Set(aud.duration_secs),
                channels: ActiveValue::Set(aud.channels),
                desp: ActiveValue::Set(aud.desp.as_ref().map(|s| s.chars().take(512).collect())),
                ..Default::default()
            })
            .collect();
        let _ = Audios::insert_many(audio_records)
            .exec(db)
            .await
            .map_err(|e| {
                error!("failed to insert images, {}", e);
                Error::Db
            });
        Ok(())
    }
}
