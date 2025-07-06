import json
import os

def load_config():
    """Load the LLM configuration from a JSON file."""
    
    config_path = os.getenv("LLM_CONFIG_PATH", "LLM.config.json")
    
    with open(config_path, "r") as file:
        config_params = json.loads(file.read())

        model_params = config_params.get("model_params", {})
    
        return model_params