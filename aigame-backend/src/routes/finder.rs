// ************************************************************************** //
//                                                                            //
//                                                        :::      ::::::::   //
//   finder.rs                                          :+:      :+:    :+:   //
//                                                    +:+ +:+         +:+     //
//   By: dfine <coding@dfine.tech>                  +#+  +:+       +#+        //
//                                                +#+#+#+#+#+   +#+           //
//   Created: 2025/03/21 11:32:35 by dfine             #+#    #+#             //
//   Updated: 2025/04/15 19:31:11 by dfine            ###   ########.fr       //
//                                                                            //
// ************************************************************************** //

use super::types::{FileType, GameModule};
use crate::utils::init::{ORIGIN_NAME, OSS_PATH};
use anyhow::{Result, anyhow};
use regex::Regex;
use std::path::{Path, PathBuf};

pub async fn generate_path(filetype: FileType, key: &str, extension: &str) -> Result<PathBuf> {
    let prefix_path: String = filetype.into();
    let dirpath = Path::new(OSS_PATH)
        .join("upload")
        .join(prefix_path)
        .join(key);
    if !dirpath.exists() {
        tokio::fs::create_dir_all(&dirpath).await?;
    }
    Ok(dirpath.join(ORIGIN_NAME).with_extension(extension))
}

pub async fn game_path(attach_key: &str) -> Result<PathBuf> {
    let dirpath = Path::new(OSS_PATH)
        .join("download")
        .join("game")
        .join(attach_key);
    if !dirpath.exists() {
        tokio::fs::create_dir_all(&dirpath).await?;
    }
    Ok(dirpath)
}
pub fn screenshot(file_key: &str) -> Option<Vec<String>> {
    let dirpath = Path::new(OSS_PATH)
        .join("upload")
        .join("ppt")
        .join(file_key)
        .join("convert")
        .join("images");
    let re = Regex::new(r"^page_(\d+)\.png$").ok()?;
    let mut files: Vec<String> = std::fs::read_dir(&dirpath)
        .ok()?
        .filter_map(|entry| {
            entry.ok().and_then(|e| {
                let name = e.file_name().into_string().ok()?;
                if re.is_match(&name) { Some(name) } else { None }
            })
        })
        .collect();
    files.sort_by_key(|f| {
        re.captures(f)
            .and_then(|c| c.get(1)?.as_str().parse::<u32>().ok())
            .unwrap_or(0)
    });
    let hostname =
        std::env::var("HOST_URL").unwrap_or("https://api.gamecreator.online".to_string());
    Some(
        files
            .into_iter()
            .map(|f| {
                let file_path = dirpath.join(&f);
                format!(
                    "{}/{}",
                    hostname.trim_end_matches("/"),
                    file_path.to_string_lossy().trim_start_matches("/")
                )
            })
            .collect(),
    )
}

pub fn find_path(filetype: FileType, key: &str, extension: &str) -> Result<PathBuf> {
    let prefix_path: String = filetype.into();
    let filepath = Path::new(OSS_PATH)
        .join("upload")
        .join(prefix_path)
        .join(key)
        .join(ORIGIN_NAME)
        .with_extension(extension);
    if !filepath.exists() {
        return Err(anyhow!("File not exist: {}", filepath.to_str().unwrap()));
    }
    Ok(filepath)
}
pub fn find_url(filetype: FileType, key: &str, extension: &str) -> Result<String> {
    let prefix_path: String = filetype.into();
    let filepath = Path::new(OSS_PATH)
        .join("upload")
        .join(prefix_path)
        .join(key)
        .join(ORIGIN_NAME)
        .with_extension(extension);
    if !filepath.exists() {
        return Err(anyhow!("File not exist: {}", filepath.to_str().unwrap()));
    }
    let hostname =
        std::env::var("HOST_URL").unwrap_or("https://api.gamecreator.online".to_string());

    Ok(format!("{}{}", hostname, filepath.to_str().unwrap()))
}

pub fn find_module(key: &str, module_type: GameModule) -> Result<PathBuf> {
    let filepath = match module_type {
        GameModule::Parse => Path::new(OSS_PATH)
            .join("upload")
            .join("ppt")
            .join(key)
            .join(module_type.filename().unwrap()),
        GameModule::Goal | GameModule::Plan | GameModule::Asset | GameModule::Code => {
            Path::new(OSS_PATH)
                .join("download")
                .join("game")
                .join(key)
                .join(module_type.filename().unwrap())
        }
        _ => return Err(anyhow!("invalid module type")),
    };
    if !filepath.exists() {
        return Err(anyhow!("File not exist: {}", filepath.to_str().unwrap()));
    }
    Ok(filepath)
}
