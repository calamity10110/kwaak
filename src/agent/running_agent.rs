
use anyhow::Result;
use std::sync::Arc;

use crate::agent::session::RunningSession;

#[derive(Clone)]
pub struct RunningAgent {
    session: Arc<RunningSession>,
}

impl RunningAgent {
    pub fn new(session: Arc<RunningSession>) -> Self {
        Self { session }
    }

    pub async fn query(&self, query: &str) -> Result<()> {
        self.session.query_agent(query).await
    }

    pub async fn run(&self) -> Result<()> {
        // This method is no longer needed, as the Python orchestrator handles the run loop.
        Ok(())
    }

    pub async fn stop(&self) {
        // This method is no longer needed, as the Python orchestrator handles its own lifecycle.
    }
}
