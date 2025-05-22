"""
Module to use OpenCV to extract features from still frames taken from video 

"""
import os 
import cv2
from typing import List, Tuple


"""Extracts video frames to be fed into feature extractor"""

def extract_frames(
        path: str,
        vid_name: str,
        fr: int = 1,
)-> None:
    # extract video raw
    cap = cv2.VideoCapture(path)

    try:
        if not os.path.exists('data' + os.sep + vid_name):
            os.makedirs('data' + os.sep + vid_name)
    except OSError:
        print('Error: data output directory already exists. You may not rewrite existing video files.')
    
    # track frame
    curr_frame = 0

    while(True):
        # read frame
        done, frame = cap.read()

        if done:
            # store frame
            nm = 'data' + os.sep + vid_name + os.sep + str(curr_frame) + '.jpg'
            cv2.imwrite(nm, frame)
            current_frame += 1
        else:
            break
