
use async_trait::async_trait;
use anyhow::Result;

#[async_trait]
pub trait LlmProvider {
    async fn generate(&self, prompt: &str) -> Result<String>;
    async fn embed(&self, text: &str) -> Result<Vec<f32>>;
}

pub struct LocalLlmProvider;

#[async_trait]
impl LlmProvider for LocalLlmProvider {
    async fn generate(&self, prompt: &str) -> Result<String> {
        Ok(format!("[local‑model‑response]: {}", prompt))
    }

    async fn embed(&self, _text: &str) -> Result<Vec<f32>> {
        Ok(vec![0.01; 16])
    }
}
