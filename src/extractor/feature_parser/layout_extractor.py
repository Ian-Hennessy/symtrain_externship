"""
Module to parse layouts provided from extracted frames by frame_extractor 
"""
import os 
import logging
from typing import List, Tuple, Dict, Any
from model import Parser
import cv2


logger = logging.getLogger(__name__)
def extract_layout(dir_path: str, model: Parser)->List[Tuple[str, int, int, int, int]]:
    """
    For each PNG in `dir_path`, run OmniParser.parse(), then convert each element's
    normalized bbox into a tuple of (feature_type, x, y, width, height).

    Args:
        dir_path: Path to a directory of `.png` images.
        model:   An instance of Parser wrapping the OmniParser model.

    Returns:
        A flat list of feature tuples.
    """
    # Initialize an empty list to store the results
    results: List[Tuple[str, int, int, int, int]] = []
    
    # Loop through each file in the directory
    for fname in os.listdir(dir_path): 
        # catch for non-image files
        if not fname.lower().endswith(".png") or not fname.lower().endswith(".jpg"):
            continue
        full_path = os.path.join(dir_path, fname)

        try :
            # parse the image using the model
            elements = model.parse(full_path)
        except RuntimeError as e:
            # log & skip failed parse
            logger.warning("Parsing failed for %s, %s", full_path, e)
            continue
        
        # load image to get dims
        img = cv2.imread(full_path)
        if img is None:
            raise FileNotFoundError(f"Could not read image at path: {full_path}")
        
        height, width, _ = img.shape

        # convert normalized bboxes 
        for e in elements:
            # finalize feature extraction by denormalizing and retrieving type
            x1, y1, x2, y2 = e['bbox']
            px = int(x1 * width)
            py = int(y1 * height)
            pw = int((x2 - x1) * width)
            ph = int((y2 - y1) * height)
            feat_type = "text" if e.get("content","").strip() else "icon"
            # append to results 
            results.append((feat_type, px, py, pw, ph))
    
    return results