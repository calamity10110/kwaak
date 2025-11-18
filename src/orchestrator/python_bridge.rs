
use anyhow::{Context, Result};
use serde::Deserialize;
use std::io::{BufReader, Write};
use std::process::{Child, Command, Stdio};
use std::sync::{Arc, Mutex};

#[derive(Deserialize, Debug)]
struct OrchestratorResult {
    agent: String,
    reply: String,
}

pub struct PythonBridge {
    child: Arc<Mutex<Child>>,
}

impl PythonBridge {
    pub fn new() -> Result<Self> {
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

        Ok(Self {
            child: Arc::new(Mutex::new(child)),
        })
    }

    pub fn query(&self, query: &str) -> Result<String> {
        let mut child = self.child.lock().unwrap();
        let stdin = child.stdin.as_mut().context("Failed to open stdin")?;
        stdin.write_all(query.as_bytes())?;
        stdin.write_all(b"\n")?;
        stdin.flush()?;

        let stdout = child.stdout.as_mut().context("Failed to open stdout")?;
        let mut reader = BufReader::new(stdout);
        let result: OrchestratorResult = rmp_serde::from_read(&mut reader)?;

        Ok(result.reply)
    }
}
