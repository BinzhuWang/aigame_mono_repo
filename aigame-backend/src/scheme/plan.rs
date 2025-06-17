use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct GamePrototype {
    module_id: u32,
    game_name: String,
    core_gameplay_summary: String,
    features: Features,
    prototype_flow: Vec<PrototypeState>,
    estimated_duration_seconds: u32,
}

#[derive(Debug, Serialize, Deserialize)]
struct Features {
    core_mechanics: Vec<String>,
    input_logic: Vec<String>,
    ui_elements: Vec<String>,
    animations_assets: Vec<String>,
    audio_feedback: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct PrototypeState {
    state: String,
    description: String,
    user_input: String,
    next_state: String,
}
