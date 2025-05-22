"""
Module to parse layouts provided from extracted frames by frame_extractor 
"""
import layoutparser as lp
import os 
from typing import List, Tuple



"""
Function to take in a path to a directory and return a list of tuples containing tuples 
of form [feature_type, x, y, width, height] for each layout image 
"""
def layout_extractor(path: str)->List[Tuple]:
    """
    Function to take in a path to a directory and return a list of tuples containing tuples 
    of form [feature_type, x, y, width, height] for each layout image 
    """
    # Get the list of all files in the directory
    files = os.listdir(path)
    
    # Initialize an empty list to store the results
    results = []
    
    # Loop through each file in the directory
    for file in files:
        # Check if the file is a .png file
        if file.endswith('.png'):
            # Create the full path to the file
            full_path = os.path.join(path, file)
            
            # Read the image using layoutparser
            image = lp.io.load_image(full_path)
            
            # Create a Layout object from the image
            layout = lp.Layout(image)
            
            # Extract features from the layout
            for feature in layout:
                results.append((feature.type, feature.x_1, feature.y_1, feature.width, feature.height))
    
    return results
    

