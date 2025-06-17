use actix_web::{
    HttpResponse,
    body::EitherBody,
    body::MessageBody,
    dev::{ServiceRequest, ServiceResponse},
    http::header,
    middleware::Next,
};
use chrono::{Duration, Utc};
use jsonwebtoken::{DecodingKey, EncodingKey, Header, TokenData, Validation, decode, encode};

use super::types::ErrCode;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct TokenClaims {
    pub iat: usize,
    pub exp: usize,
}
#[derive(Debug, Clone)]
pub struct JwtConf {
    pub secret: String,
    pub expire: i64,
}
pub fn encode_jwt(jwt_conf: JwtConf) -> Result<String, ErrCode> {
    let now = Utc::now();

    let expire = Duration::hours(jwt_conf.expire);
    let claims = TokenClaims {
        iat: now.timestamp() as usize,
        exp: (now + expire).timestamp() as usize,
    };
    encode(
        &Header::default(),
        &claims,
        &EncodingKey::from_secret(jwt_conf.secret.as_bytes()),
    )
    .map_err(|_| ErrCode::UnKnown)
}

pub fn decode_jwt(token: &str, jwt_conf: JwtConf) -> Result<TokenData<TokenClaims>, String> {
    println!("accept jwt token:{}", token);
    if let Ok(token_data) = decode::<TokenClaims>(
        token,
        &DecodingKey::from_secret(jwt_conf.secret.as_bytes()),
        &Validation::default(),
    ) {
        let now = Utc::now().timestamp() as usize;
        if token_data.claims.exp < now {
            println!("token expired");
            return Err("Expired token".to_string());
        }
        return Ok(token_data);
    }
    println!("invalid token");
    Err("Invalid token".to_string())
}

pub async fn auth_middleware(
    req: ServiceRequest,
    next: Next<impl MessageBody>,
) -> Result<ServiceResponse<EitherBody<impl MessageBody>>, actix_web::Error> {
    let secret = std::env::var("JWT_SECRET").unwrap_or_else(|_| "aigame".to_string());
    let expire = std::env::var("JWT_EXPIRATION_TIME")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(3600);

    let authorized = req
        .headers()
        .get(header::AUTHORIZATION)
        .and_then(|v| v.to_str().ok())
        .map(|token| {
            let token_trim = token.trim_start_matches("Bearer ").trim();
            decode_jwt(token_trim, JwtConf { secret, expire }).is_ok()
        })
        .unwrap_or(false);
    if !authorized {
        let response = req.into_response(
            HttpResponse::Unauthorized()
                .body("Unauthorized")
                .map_into_right_body(),
        );
        return Ok(response);
    }
    let res = next.call(req).await?;
    Ok(res.map_into_left_body())
}
