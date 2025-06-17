use super::{
    AppState, finder,
    types::{ErrCode, Error, GameModule, GenericBody},
};
use crate::db::gamecases::{self, Entity as GameCases};
use actix_web::{Responder, Scope, post, web};
use sea_orm::EntityTrait;
use serde::{Deserialize, Serialize};
use tracing::*;

#[derive(Serialize, Deserialize, Clone)]
enum FeedbackType {
    #[serde(rename = "sandbox_debug")]
    SandboxDebug,
    #[serde(rename = "user_ask")]
    UserAsk,
    #[serde(rename = "screenshot")]
    Screenshot,
}

#[derive(Serialize, Deserialize, Clone)]
struct FeedInfo {
    feedback_type: FeedbackType,
    content: String,
}
#[derive(Serialize, Deserialize, Clone)]
struct ChatInfo {
    game_id: i32,
    content: Vec<FeedInfo>,
}

#[derive(Serialize, Deserialize)]
struct RequestInfo {
    game_path: String,
    content: Vec<FeedInfo>,
}

#[derive(Debug, Serialize, Deserialize)]
struct CodeResult {
    code: String,
}

#[derive(Deserialize)]
struct ApiResponse {
    status: String,
    code: i32,
    msg: String,
    result: Option<CodeResult>,
}

#[post("/code")]
async fn chat_stream(
    app_state: web::Data<AppState>,
    chat_info: web::Json<ChatInfo>,
) -> Result<impl Responder, Error> {
    let game = match GameCases::find_by_id(chat_info.game_id)
        .one(&app_state.db)
        .await
        .map_err(|_| Error::Db)?
    {
        Some(game) => game,
        None => {
            error!("invalid game id");
            return Ok(GenericBody::err(ErrCode::DataBase));
        }
    };
    let game_path = finder::game_path(game.file_key.as_ref())
        .await
        .map_err(|e| {
            error!("failed to find game path: {}", e);
            Error::Io
        })?;
    let request_info = RequestInfo {
        game_path: game_path
            .to_str()
            .ok_or_else(|| {
                error!("Path contains non-UTF-8 characters: {:?}", game_path);
                Error::Format
            })?
            .to_string(),
        content: chat_info.content.clone(),
    };

    let tools_url = std::env::var("TOOLS_URL").unwrap_or("http://aigame-tools".to_string());
    let client = reqwest::Client::new();
    let res = client
        .post(format!(
            "{}/chat",
            tools_url.strip_suffix("/").unwrap_or(&tools_url)
        ))
        .json(&request_info)
        .send()
        .await
        .map_err(|e| {
            error!("failed to request chat: {}", e);
            Error::Network
        })?;
    let response = res.error_for_status().map_err(|e| {
        error!("failed to request chat: {}", e);
        Error::Network
    })?;
    let api_response: ApiResponse = response.json().await.map_err(|e| {
        error!("failed to request chat: {}", e);
        Error::Format
    })?;
    if api_response.code != 200 || api_response.result.is_none() {
        return Ok(GenericBody::err(ErrCode::Custom(api_response.msg)));
    }

    Ok(GenericBody::new(
        "chat code finished",
        Some(api_response.result),
    ))
}

pub fn routes() -> Scope {
    web::scope("/chat").service(chat_stream)
}
