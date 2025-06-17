// ************************************************************************** //
//                                                                            //
//                                                        :::      ::::::::   //
//   init.rs                                            :+:      :+:    :+:   //
//                                                    +:+ +:+         +:+     //
//   By: dfine <coding@dfine.tech>                  +#+  +:+       +#+        //
//                                                +#+#+#+#+#+   +#+           //
//   Created: 2025/03/20 20:09:33 by dfine             #+#    #+#             //
//   Updated: 2025/04/15 20:42:54 by dfine            ###   ########.fr       //
//                                                                            //
// ************************************************************************** //

use anyhow::{Context, Result, anyhow};
use sea_orm::{ConnectOptions, Database, DatabaseConnection};
use tokio::time::Duration;
use tracing::*;
pub static OSS_PATH: &str = "/data";
pub static ORIGIN_NAME: &str = "origin";
pub static PPT_FORMATS: &[&str] = &["ppt", "pptx"];
pub static IMAGE_FORMATS: &[&str] = &["jpg", "png"];
pub static AUDIO_FORMATS: &[&str] = &["mp3", "wav"];
pub static VIDEO_FORMATS: &[&str] = &["mp4", "mkv"];

pub async fn init_db(uri: &str) -> Result<DatabaseConnection> {
    let mut opt = ConnectOptions::new(uri);
    opt.max_connections(100)
        .min_connections(5)
        .connect_timeout(Duration::from_secs(30))
        .acquire_timeout(Duration::from_secs(30))
        .idle_timeout(Duration::from_secs(30))
        .max_lifetime(Duration::from_secs(30))
        .sqlx_logging(false)
        .sqlx_logging_level(log::LevelFilter::Info);
    Database::connect(opt)
        .await
        .map_err(|e| anyhow!(e))
        .context("Failed to connect to the database")
}
