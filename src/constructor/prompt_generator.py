"""
Take a list of tuples containing (feature_type, x, y, width, height) and convert them into a string prompt for 
a code-generation model. They should be specific, concise, and direct. 
"""
import os 
from typing import List, Tuple
from openai import OpenAI


def generate_prompt(features: List[Tuple[str, int, int, int, int]], canvas = (1024, 768)) -> str:
    """
    Generate a prompt string from a list of feature tuples.

    Args:
        features: A list of tuples, each containing (feature_type, x, y, width, height).

    Returns:
        A string prompt for code generation.
    """
    prompt = str(
        "Context:\n"
        "You are a code generator that produces a complete, runnable UI mockup as HTML/CSS (no explanations)."
        "This mockup will be used as a sandbox tutorial for call center trainees.\n\n"
        "Return a complete HTML/CSS mockup based on the following features.\n"
        "Requirements:\n"
        f"- Canvas size: {canvas[0]}×{canvas[1]} px. Coordinates are in pixels with the origin at the top-left corner.\n"
        "- Use CSS Grid or Flexbox to position elements.\n"
        "- Map each feature to a semantic HTML element with styling.\n"
        "Map feature_type='button' to <button>, feature_type='text' to <p> or <input type='text'> as appropriate.\n"
        "You don't need colors or fonts—focus on positioning and basic borders. \n"
        "Respond only with a single markdown code block labeled html."
        "- Return only code (HTML, CSS, JS if needed).\n\n"
        "Elements:\n"
    )
    
    for feature in features:
        feature_type, x, y, width, height = feature
        prompt += f"- {feature_type} at ({x}, {y}), size ({width}x{height})\n"
    
    return prompt

def html_generator(prompt: str) -> str:
    """
    Send prompt to GPT instance using OpenAI API. Return generated code and write 
    to .html file for serving to the frontend renderer 
    """

    # placeholder for openAI api key 
    key = "placeholder"

    # establish client 
    client = OpenAI(key)

    # send prompt to model for html generation 
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        input = prompt)

    
    # write generated response to .html file 
    generated_html = response.choices[0].message.content.strip()
    if not os.path.exists("demo/tests/"):
        os.makedirs("demo/tests/")
    html_file_path = "demo/tests/generated_mockup.html"
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(generated_html)



    