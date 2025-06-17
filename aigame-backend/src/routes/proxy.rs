use std::time::Duration;

use actix_proxy::{IntoHttpResponse, SendRequestError};
use actix_web::{
    HttpResponse, Scope, post,
    web::{self, scope},
};
use awc::Client;
use tracing::info;

#[post("/{url:.*}")]
async fn proxy_post(
    path: web::Path<(String,)>,
    body: web::Bytes,
    client: web::Data<Client>,
) -> Result<HttpResponse, SendRequestError> {
    let (url,) = path.into_inner();
    let tools_url = std::env::var("TOOLS_URL").unwrap_or("http://aigame-tools".to_string());
    let forward_url = format!(
        "{}/{}",
        tools_url.strip_suffix("/").unwrap_or(&tools_url),
        url
    );
    info!("accept request from {}, proxy to {}", url, &forward_url);
    Ok(client
        .post(forward_url)
        .send_body(body)
        .await?
        .into_http_response())
}

pub fn routes() -> Scope {
    scope("/proxy")
        .app_data(web::Data::new(
            Client::builder()
                .timeout(Duration::from_secs(3600))
                .finish(),
        ))
        .service(proxy_post)
}
