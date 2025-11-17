
# Kwaak + LLM Orchestrator: Installation and Usage

This document provides detailed instructions on how to set up and run the integrated Kwaak application with the Python-based LLM Orchestrator.

## 1. Installation

This project has two parts: a Rust-based TUI application (Kwaak) and a Python-based LLM orchestrator. You will need to install dependencies for both.

### Python Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Rust Dependencies

You will need to have the Rust toolchain installed. You can then build the Kwaak application using Cargo:

```bash
cargo build
```

## 2. Configuration

The orchestrator's behavior is configured through a `config.json` file. An example configuration is provided in `examples/simple_project/config.json`.

### Using the Configuration Script

The easiest way to configure the LLM provider is to use the `configure_provider.py` script:

```bash
python3 scripts/configure_provider.py
```

### Manual Configuration

You can also configure the provider manually by editing `examples/simple_project/config.json`.

#### LLM Providers

You can choose between two LLM providers: `local` and `openai`.

##### OpenAI Provider

To use the `openai` provider, you need to provide your OpenAI API key. Create a `.env` file in the root of the project (you can copy `.env.example`) and add your API key:

```
OPENAI_API_KEY="your-api-key"
```

## 3. Running the Application

To run the integrated application, you will start the Kwaak TUI. Kwaak will automatically run the Python orchestrator in the background.

```bash
cargo run
```

When you start a new chat in the Kwaak TUI, it will:

1.  Spawn the Python orchestrator service.
2.  Send the prompt to the orchestrator.
3.  Receive the response from the orchestrator and display it in the chat.
