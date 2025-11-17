
import asyncio
import os
from dotenv import load_dotenv
from orchestrator.main import LLMOrchestrator
from orchestrator.core.config import OrchestratorConfig
from orchestrator.project.initializer import ProjectInitializer

# Load environment variables from .env file
load_dotenv()

async def main():
    # Correct the path to be relative to the script's location
    script_dir = os.path.dirname(__file__)
    config_path = os.path.join(script_dir, 'simple_project', 'config.json')

    # Load configuration
    config = OrchestratorConfig.load(config_path)

    # Note to the user
    if config.llm_provider == "openai":
        if not os.environ.get("OPENAI_API_KEY"):
            print("Please set the OPENAI_API_KEY environment variable to run the example with the OpenAI provider.")
            return

    # Initialize the orchestrator
    orchestrator = LLMOrchestrator(config)

    # Initialize the project
    project_initializer = ProjectInitializer(orchestrator)
    project_meta = await project_initializer.init()

    print("Project initialized successfully!")
    print(f"Project metadata: {project_meta}")

    # Run a simple agent task
    agent_name = "project_pri"
    prompt = "Hello, agent!"

    # Load the agent to ensure it is available
    orchestrator.agents.load()

    result = await orchestrator.run(agent_name, prompt)

    print(f"Agent '{agent_name}' replied: {result.get('reply', 'No reply')}")

if __name__ == "__main__":
    asyncio.run(main())
