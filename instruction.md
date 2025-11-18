
# Kwaak: Installation and Usage

This document provides detailed instructions on how to set up and run the Kwaak application.

## 1. Installation

You will need to have the Rust toolchain installed. You can then build the Kwaak application using Cargo:

```bash
cargo build
```

## 2. Configuration

Kwaak's behavior is configured through a `kwaak.toml` file. You can create a `kwaak.toml` file in the root of the project to configure the application.

### LLM Provider

The orchestrator's LLM provider is configured in the `[orchestrator]` section of your `kwaak.toml`.

#### Local Provider

The `local` provider is a simple, offline provider that is useful for testing and development. To use it, set the `llm_provider` to `"local"`:

```toml
[orchestrator]
llm_provider = "local"
```

## 3. Running the Application

To run the Kwaak TUI, use the `cargo run` command:

```bash
cargo run
```

When you start a new chat in the Kwaak TUI, it will:

1.  Initialize the orchestrator with the settings from `kwaak.toml`.
2.  Run a simple agent task and print the response to the console.
