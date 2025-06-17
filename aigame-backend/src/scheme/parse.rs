use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct Evidence {
    page: u32,
    text_excerpt: String,
    image_summary: String,
}

#[derive(Serialize, Deserialize)]
struct Module {
    start_page: u32,
    end_page: u32,
    game_goal: String,
    evidence: Vec<Evidence>,
}

#[derive(Serialize, Deserialize)]
struct Root {
    modules: Vec<Module>,
}
