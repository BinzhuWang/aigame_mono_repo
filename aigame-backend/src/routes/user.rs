// ************************************************************************** //
//                                                                            //
//                                                        :::      ::::::::   //
//   user.rs                                            :+:      :+:    :+:   //
//                                                    +:+ +:+         +:+     //
//   By: dfine <coding@dfine.tech>                  +#+  +:+       +#+        //
//                                                +#+#+#+#+#+   +#+           //
//   Created: 2025/03/20 20:10:01 by dfine             #+#    #+#             //
//   Updated: 2025/04/20 23:49:32 by dfine            ###   ########.fr       //
//                                                                            //
// ************************************************************************** //

use super::auth;
use super::types::{self, ErrCode, GenericBody};
use actix_web::{Responder, Scope, post, web};
use serde::Deserialize;

#[derive(Deserialize)]
struct UserInfo {
    username: String,
    password: String,
}

#[post("/login")]
async fn login(user_info: web::Json<UserInfo>) -> Result<impl Responder, types::Error> {
    let default_user = std::env::var("ADMIN_USER").unwrap_or("admin".to_string());
    let default_password = std::env::var("ADMIN_PASSWORD").unwrap_or("aigame-25".to_string());
    if user_info.username != default_user || user_info.password != default_password {
        return Ok(GenericBody::err(ErrCode::Param));
    }
    let secret = std::env::var("JWT_SECRET").unwrap_or("aigame".to_string());
    let expire = std::env::var("JWT_EXPIRATION_TIME")
        .ok()
        .and_then(|v| v.parse::<i64>().ok())
        .unwrap_or(3600);

    match auth::encode_jwt(auth::JwtConf { secret, expire }) {
        Ok(jwt_token) => Ok(GenericBody::new("login succeed", Some(jwt_token))),
        Err(e) => Ok(GenericBody::err(e)),
    }
}

pub fn routes() -> Scope {
    web::scope("/user").service(login)
}
