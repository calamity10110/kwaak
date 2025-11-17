
use anyhow::{Context, Result};
use serde::Deserialize;
use std::io::{BufReader, Read, Write};
use std::process::{Child, Command, Stdio};
use std::sync::{Arc, Mutex};
use tokio::sync::mpsc::UnboundedSender;
use tokio_util::sync::CancellationToken;
use uuid::Uuid;

use crate::{
    commands::Responder,
    config,
    indexing::Index,
    repository::Repository,
};

use super::running_agent::RunningAgent;

#[derive(Clone)]
pub struct Session {
    pub session_id: Uuid,
    pub repository: Arc<Repository>,
    pub default_responder: Arc<dyn Responder>,
    pub initial_query: String,
    running_session_tx: UnboundedSender<SessionMessage>,
}

#[derive(Clone)]
pub enum SessionMessage {
    SwapAgent(RunningAgent),
}

impl Session {
    pub fn builder() -> SessionBuilder {
        SessionBuilder::default()
    }
}

#[derive(Default)]
pub struct SessionBuilder {
    session_id: Option<Uuid>,
    repository: Option<Arc<Repository>>,
    default_responder: Option<Arc<dyn Responder>>,
    initial_query: Option<String>,
    running_session_tx: Option<UnboundedSender<SessionMessage>>,
}

impl SessionBuilder {
    pub fn session_id(&mut self, session_id: Uuid) -> &mut Self {
        self.session_id = Some(session_id);
        self
    }

    pub fn repository(&mut self, repository: Arc<Repository>) -> &mut Self {
        self.repository = Some(repository);
        self
    }

    pub fn default_responder(&mut self, default_responder: Arc<dyn Responder>) -> &mut Self {
        self.default_responder = Some(default_responder);
        self
    }

    pub fn initial_query(&mut self, initial_query: String) -> &mut Self {
        self.initial_query = Some(initial_query);
        self
    }

    pub fn running_session_tx(
        &mut self,
        running_session_tx: UnboundedSender<SessionMessage>,
    ) -> &mut Self {
        self.running_session_tx = Some(running_session_tx);
        self
    }

    pub async fn start(&self, _index: &(impl Index + 'static + Clone)) -> Result<RunningSession> {
        let (running_session_tx, _) = tokio::sync::mpsc::unbounded_channel();

        let session = Arc::new(Session {
            session_id: self.session_id.context("session_id not set")?,
            repository: self.repository.clone().context("repository not set")?,
            default_responder: self
                .default_responder
                .clone()
                .context("default_responder not set")?,
            initial_query: self.initial_query.clone().context("initial_query not set")?,
            running_session_tx,
        });

        let python_executable = "python3";
        let script_path = "orchestrator_service.py";
        let config_path = "examples/simple_project/config.json";

        let child = Command::new(python_executable)
            .arg(script_path)
            .env("KWAAK_CONFIG_PATH", config_path)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()?;

        Ok(RunningSession {
            session,
            child: Arc::new(Mutex::new(child)),
            cancel_token: Arc::new(Mutex::new(CancellationToken::new())),
        })
    }
}

pub struct RunningSession {
    pub session: Arc<Session>,
    child: Arc<Mutex<Child>>,
    cancel_token: Arc<Mutex<CancellationToken>>,
}

#[derive(Deserialize, Debug)]
struct OrchestratorResult {
    agent: String,
    reply: String,
}

impl RunningSession {
    pub async fn query_agent(&self, query: &str) -> Result<()> {
        let mut child = self.child.lock().unwrap();
        let stdin = child.stdin.as_mut().context("Failed to open stdin")?;
        stdin.write_all(query.as_bytes())?;
        stdin.write_all(b"\n")?;
        stdin.flush()?;

        let stdout = child.stdout.as_mut().context("Failed to open stdout")?;
        let mut reader = BufReader::new(stdout);
        let result: OrchestratorResult = rmp_serde::from_read(&mut reader)?;

        self.session.default_responder.update(&result.reply).await;

        Ok(())
    }

    pub fn cancel_token(&self) -> CancellationToken {
        self.cancel_token.lock().unwrap().clone()
    }
}
