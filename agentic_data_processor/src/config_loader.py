# src/config_loader.py

import yaml

def load_agent_config(config_path='configs/agent_config.yaml'):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config
