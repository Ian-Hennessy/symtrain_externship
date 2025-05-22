import json
from transformers import pipeline
from typing import List, Dict, Any

class Parser:
    def __init__(
        self,
        model_name: str = "microsoft/OmniParser",
        device: int = 0   # set to -1 for CPU only
    ):
        """
        Wraps Hugging Face's 'image-text-to-text' pipeline for OmniParser.
        
        Args:
          model_name: name of the HF model to load.
          device: CUDA device index (e.g. 0), or -1 for CPU.
        """
        self.pipe = pipeline(
            "image-text-to-text",
            model=model_name,
            device=device
        )  # returns [{'generated_text': ...}]
    
    def parse(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Run OmniParser on a single screenshot or video frame and return structured JSON.
        
        Args:
          image_path: path to your PNG/JPEG screenshot.
        Returns:
          A list of element-dicts, each with keys like
          'id', 'bbox', 'content', 'interactivity', etc.
        """
        outputs = self.pipe(image_path)
        text = outputs[0].get("generated_text", "")
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise RuntimeError(f"Failed to parse JSON from model output:\n{text}")
    
    def parse_batch(self, paths: List[str]) -> List[List[Dict[str, Any]]]:
        """
        Parse multiple screenshots in sequence.
        """
        return [ self.parse(p) for p in paths ]

    

    


