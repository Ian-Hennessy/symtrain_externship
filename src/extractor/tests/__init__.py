import model
import os 
import cv2
from feature_parser import layout_extractor
from feature_parser import frame_extractor

def __init__() -> None:
    """Initialize the test module."""
    m = model.Parser()
    
    # load data 
    dpath = "data"
    if not os.path.exists(dpath):
        raise FileNotFoundError("Data directory does not exist.")


    
    pass