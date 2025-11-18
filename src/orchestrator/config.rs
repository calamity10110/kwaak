
use serde::Deserialize;
use std::collections::HashMap;

#[derive(Deserialize, Debug, Clone)]
pub struct OrchestratorConfig {
    pub llm_provider: String,
    pub provider_settings: Option<HashMap<String, String>>,
}
