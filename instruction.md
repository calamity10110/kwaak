
# LLM Orchestrator Library: Installation and Usage

This document provides detailed instructions on how to set up and run the LLM Orchestrator library.

## 1. Installation

First, you need to install the required Python packages. You can do this using pip:

```bash
pip install msgpack chromadb openai
```

## 2. Configuration

The orchestrator's behavior is configured through a `config.json` file. An example configuration is provided in `examples/simple_project/config.json`.

### LLM Providers

You can choose between two LLM providers: `local` and `openai`.

#### Local Provider

The `local` provider is a simple, offline provider that is useful for testing and development. To use it, set the `llm_provider` to `"local"` in your `config.json`:

```json
{
  "llm_provider": "local"
}
```

#### OpenAI Provider

The `openai` provider uses the OpenAI API to generate responses and embeddings. To use it, you need to:

1.  **Set the `llm_provider` to `"openai"`** in your `config.json`.
2.  **Provide your OpenAI API key.** The library will look for the `OPENAI_API_KEY` environment variable. You can set it in your shell like this:

    ```bash
    export OPENAI_API_KEY="your-api-key"
    ```

3.  **Configure the model (optional).** You can specify which OpenAI model to use in the `provider_settings` section of your `config.json`. If you don't specify a model, it will default to `"gpt-3.5-turbo"`.

    ```json
    {
      "llm_provider": "openai",
      "provider_settings": {
        "model": "gpt-4"
      }
    }
    ```

## 3. Running the Example

An example project is provided in the `examples/simple_project` directory. To run it, execute the `run_simple_project.py` script from the root of the project:

```bash
PYTHONPATH=. python3 examples/run_simple_project.py
```

**Note:** You must set the `PYTHONPATH` to `.` for the script to be able to find the `orchestrator` library.

When you run the example, it will:

1.  Initialize the orchestrator with the settings from `examples/simple_project/config.json`.
2.  Create a `db` directory in `examples/simple_project` to store the project's memory.
3.  Create an `agent.md` file in `examples/simple_project` if one doesn't already exist.
4.  Run a simple agent task and print the response to the console.
