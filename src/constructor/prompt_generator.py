"""
Take a list of tuples containing (feature_type, x, y, width, height) and convert them into a string prompt for 
a code-generation model. They should be specific, concise, and direct. 
"""
from typing import List, Tuple


def generate_prompt(features: List[Tuple[str, int, int, int, int]], canvas = (1024, 768)) -> str:
    """
    Generate a prompt string from a list of feature tuples.

    Args:
        features: A list of tuples, each containing (feature_type, x, y, width, height).

    Returns:
        A string prompt for code generation.
    """
    prompt = (
        "Context:\n"
        "You are a code generator that produces a complete, runnable UI mockup as HTML/CSS (no explanations)."
        " This mockup will be used as a sandbox tutorial for call center trainees.\n\n"
        "Requirements:\n"
        f"- Canvas size: {canvas[0]}×{canvas[1]} px.\n"
        "- Use CSS Grid or Flexbox to position elements.\n"
        "- Map each feature to a semantic HTML element with styling.\n"
        "- Return only code (HTML, CSS, JS if needed).\n\n"
        "Elements:\n"
    )
    
    for feature in features:
        feature_type, x, y, width, height = feature
        prompt += f"- {feature_type} at ({x}, {y}), size ({width}x{height})\n"
    
    return prompt