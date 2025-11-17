
import asyncio
import sys
import os
from dotenv import load_dotenv

from orchestrator.main import LLMOrchestrator
from orchestrator.core.config import OrchestratorConfig
from orchestrator.core.protocol import CompactProtocol

# Load environment variables from .env file
load_dotenv()

async def main():
    # Get the config path from an environment variable
    config_path = os.environ.get("KWAAK_CONFIG_PATH")
    if not config_path:
        raise ValueError("KWAAK_CONFIG_PATH environment variable not set.")

    # Load configuration
    config = OrchestratorConfig.load(config_path)

    # Initialize the orchestrator
    orchestrator = LLMOrchestrator(config)

    # Run in a loop
    while True:
        # Read the prompt from stdin
        prompt = sys.stdin.readline()
        if not prompt:
            break

        # Run a simple agent task
        agent_name = "project_pri"
        result = await orchestrator.run(agent_name, prompt.strip())

        # Write the result to stdout
        encoded_result = CompactProtocol.encode(result)
        sys.stdout.buffer.write(encoded_result)
        sys.stdout.buffer.flush()

if __name__ == "__main__":
    asyncio.run(main())
