
# LLM Orchestrator Library

The LLM Orchestrator Library is a fully modular, async, extensible, typed, secure, multi-agent, and multi-LLM framework designed to provide a robust foundation for building sophisticated LLM-powered applications.

## Vision

Our goal is to create a comprehensive orchestration framework that supports:

- **Multi-Agent Systems:** With primary and minion agents that can be activated and deactivated as needed.
- **Structured Memory:** Using a unified database for memory, tools, agent info, and project metadata.
- **Retrieval-Augmented Generation (RAG):** To provide LLMs with relevant context for more informed responses.
- **Cloud and Local LLMs:** With support for providers like OpenAI and local models.
- **A Rich TUI:** With VSCode-style panels for a seamless user experience.

## Key Features (Implemented)

- **Modular Architecture:** The library is structured into logical sub-packages for core components, agents, tools, storage, LLM providers, and project management.
- **Async-First Design:** All LLM calls, DB queries, and tool executions are asynchronous for high performance.
- **Cloud and Local LLM Support:** The library supports both a simple `local` LLM provider for testing and an `openai` provider for cloud-based generation and embeddings.
- **Structured RAG:** The orchestrator can retrieve relevant information from its memory to provide context to the LLM, resulting in more informed responses.

## Getting Started

For detailed instructions on how to install, configure, and run the LLM Orchestrator library, please see [instruction.md](instruction.md).
