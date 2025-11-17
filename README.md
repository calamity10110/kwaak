
# Kwaak + LLM Orchestrator

This project integrates the Rust-based Kwaak TUI with a Python-based LLM Orchestrator library, creating a powerful and flexible framework for building AI-powered applications.

## Architecture

The integrated application uses a two-process architecture:

-   **Kwaak (Rust):** The main application, which provides the terminal-based user interface (TUI).
-   **LLM Orchestrator (Python):** A separate process that is spawned by Kwaak to handle all agent-related tasks, including LLM calls, tool execution, and memory management.

This architecture allows us to leverage the strengths of both Rust (for a fast and responsive TUI) and Python (for a rich and flexible AI ecosystem).

## Key Features

- **Modular and Extensible:** The Python orchestrator is designed to be highly modular, making it easy to add new agents, tools, and LLM providers.
- **Async-First Design:** The orchestrator is built on an async-first architecture for high performance.
- **Cloud and Local LLM Support:** The orchestrator supports both local and cloud-based LLMs, including OpenAI.
- **Structured RAG:** The orchestrator uses Retrieval-Augmented Generation (RAG) to provide LLMs with relevant context, resulting in more informed responses.

## Getting Started

For detailed instructions on how to install, configure, and run the integrated application, please see [instruction.md](instruction.md).
