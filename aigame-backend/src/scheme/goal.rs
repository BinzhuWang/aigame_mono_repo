use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct GoalSet {
    modules: Vec<Module>,
}

#[derive(Debug, Serialize, Deserialize)]
struct Module {
    start_page: u32,
    end_page: u32,
    game_goal: String,
    evidence: Vec<Evidence>,
}

#[derive(Debug, Serialize, Deserialize)]
struct Evidence {
    page: u32,
    text_excerpt: String,
    image_summary: String,
}
