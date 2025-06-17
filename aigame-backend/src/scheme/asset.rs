use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct GameAsset {
    asset_name: String,
    r#type: String,
    resolution: Option<String>,
    duration: Option<String>,
    fps: Option<i32>,
    reference: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct AssetList {
    asset_list: Vec<GameAsset>,
}
