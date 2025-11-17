
import json
import os

def configure_provider():
    config_path = os.path.join("examples", "simple_project", "config.json")

    # Read the existing config
    with open(config_path, "r") as f:
        config = json.load(f)

    print("LLM Provider Configuration")
    print("==========================")

    # Choose the provider
    print("\nSelect an LLM provider:")
    print("1. Local (for testing and development)")
    print("2. OpenAI (requires an API key)")

    provider_choice = input("Enter the number of your choice: ")

    if provider_choice == "1":
        config["llm_provider"] = "local"
        config["provider_settings"] = {}
        print("Provider set to 'local'.")
    elif provider_choice == "2":
        config["llm_provider"] = "openai"

        # Get the model
        model = input("Enter the OpenAI model to use (e.g., gpt-3.5-turbo): ")
        config["provider_settings"] = {"model": model}

        # Check for API key
        if not os.environ.get("OPENAI_API_KEY"):
            print("\nWarning: The OPENAI_API_KEY environment variable is not set.")
            print("Please create a .env file with your API key or set it in your shell.")

        print("Provider set to 'openai'.")
    else:
        print("Invalid choice. No changes were made.")
        return

    # Write the updated config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print("\nConfiguration updated successfully!")

if __name__ == "__main__":
    configure_provider()
