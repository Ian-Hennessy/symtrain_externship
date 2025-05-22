"""
This script is used to train a model using the provided training data. UNUSED FOR NOW - OmniParser comes 
pretrained, and data for additional training isn't currently available. Model will need additional, targeted training 
for Symtrain-specific use cases, but is okay as-is for Proof of Concept/MVP purposes. 
"""
import os 
import json
from model import Parser
from typing import List, Dict, Any

def train_model(model: Parser, data_path: str) -> None:
    # check for failure to access path:
    if (not os.path.exists(data_path)):
        raise FileNotFoundError(f"Data path {data_path} does not exist.")
    if (not os.path.isdir(data_path)):
        raise NotADirectoryError(f"Data path {data_path} is not a directory.")
    
    # check for null model:
    if (model is None):
        raise ValueError("The model you are trying to access does not exist. Please create or reinitialize and try again.")
    
    # check for empty data
    if (not os.listdir(data_path)):
        raise ValueError(f"Data path {data_path} is empty. Please provide valid training data.")
    # check for invalid data
    for file in os.listdir(data_path):
        if not file.endswith('.json'):
            raise ValueError(f"Invalid data file: {file}. Expected .json files.")
        
    # load training data
    training_data = []
    for file in os.listdir(data_path):
        if file.endswith('.json'):
            with open(os.path.join(data_path, file), 'r') as f:
                data = json.load(f)
                training_data.append(data)

    