
use std::{
    future::Future,
    pin::Pin,
    sync::{Arc, Mutex},
};

use anyhow::{Context as _, Result};
use derive_builder::Builder;
use rmcp::{
    ServiceExt as _,
    model::{ClientInfo, Implementation},
    transport::TokioChildProcess,
};
use swiftide::{
    agents::{AgentBuilder, tools::mcp::McpToolbox},
    chat_completion::{ParamSpec, Tool, ToolSpec},
    traits::{SimplePrompt, ToolBox, ToolExecutor},
};
use tavily::Tavily;
use tokio::sync::mpsc::UnboundedSender;
use tokio_util::{sync::CancellationToken, task::AbortOnDropHandle};
use uuid::Uuid;

use crate::{
    agent::{tools::DelegateAgent, util},
    commands::Responder,
    config::{self, AgentEditMode, mcp::McpServer},
    indexing::Index,
    orchestrator::python_bridge::PythonBridge,
    repository::Repository,
};

use super::{
    agents, git_agent_environment::GitAgentEnvironment, running_agent::RunningAgent, tools,
};

pub type OnAgentBuildFn = Arc<
    dyn for<'a> Fn(&'a mut AgentBuilder) -> Pin<Box<dyn Future<Output = Result<()>> + Send + 'a>>
        + Send
        + Sync,
>;

/// Session represents the abstract state of an ongoing agent interaction (i.e. in a chat)
#[derive(Clone, Builder)]
#[builder(build_fn(private), setter(into))]
pub struct Session {
    pub session_id: Uuid,
    pub repository: Arc<Repository>,
    pub default_responder: Arc<dyn Responder>,
    pub initial_query: String,

    /// Optionally run a callback on the agent builder before starting the session
    pub on_agent_build: Option<OnAgentBuildFn>,

    /// Handle to send messages to the running session
    running_session_tx: UnboundedSender<SessionMessage>,
}

/// Messages that can be send from i.e. a tool to an active session
#[derive(Clone)]
pub enum SessionMessage {
    SwapAgent(RunningAgent),
}

impl std::fmt::Debug for SessionMessage {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::SwapAgent(_) => f.debug_tuple("SwapAgent").finish(),
        }
    }
}

impl Session {
    #[must_use]
    pub fn builder() -> SessionBuilder {
        SessionBuilder::default()
    }

    /// Inform the running session that the agent has been swapped
    pub fn swap_agent(&self, agent: RunningAgent) -> Result<()> {
        self.running_session_tx
            .send(SessionMessage::SwapAgent(agent))
            .map_err(Into::into)
    }
}

impl SessionBuilder {
    /// Starts a session
    #[tracing::instrument(skip_all)]
    pub async fn start(
        &mut self,
        index: &(impl Index + 'static + Clone),
    ) -> Result<RunningSession> {
        let (running_session_tx, running_session_rx) = tokio::sync::mpsc::unbounded_channel();

        let session = Arc::new(
            self.running_session_tx(running_session_tx)
                .build()
                .context("Failed to build session")?,
        );

        let python_bridge = PythonBridge::new()?;

        let mut running_session = RunningSession {
            session,
            python_bridge: Arc::new(python_bridge),
            cancel_token: Arc::new(Mutex::new(CancellationToken::new())),
            message_task_handle: None,
        };

        let handle = tokio::spawn(running_message_handler(
            running_session.clone(),
            running_session_rx,
        ));

        running_session.message_task_handle = Some(Arc::new(AbortOnDropHandle::new(handle)));

        Ok(running_session)
    }
}

/// Spawns a small task to handle messages sent to the active session
async fn running_message_handler(
    _running_session: RunningSession,
    mut running_session_rx: tokio::sync::mpsc::UnboundedReceiver<SessionMessage>,
) {
    while let Some(message) = running_session_rx.recv().await {
        tracing::debug!(?message, "Session received message");
    }
}

/// References a running session
#[derive(Clone)]
pub struct RunningSession {
    session: Arc<Session>,
    python_bridge: Arc<PythonBridge>,
    message_task_handle: Option<Arc<AbortOnDropHandle<()>>>,
    cancel_token: Arc<Mutex<CancellationToken>>,
}

impl RunningSession {
    /// Run an agent with a query
    pub async fn query_agent(&self, query: &str) -> Result<()> {
        let response = self.python_bridge.query(query)?;
        self.session.default_responder.update(&response).await;
        Ok(())
    }

    /// Retrieve a copy of the cancel token
    #[must_use]
    pub fn cancel_token(&self) -> CancellationToken {
        self.cancel_token.lock().unwrap().clone()
    }
}
