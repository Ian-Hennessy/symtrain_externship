"""
Module to use OpenCV to extract features from still frames taken from video 

"""
import os 
import cv2
from typing import List, Tuple


"""Extracts video frames to be fed into feature extractor"""

def extract_frames(
        vid_path: str, # the path to the video. should end in .mp4, .avi, etc.
        dir_name: str, # output directory name. Append to data/..
        out_root: str = 'data', # root directory to write output to
        fr: int = 1,
)-> None:
    # sanity checks 
    if (vid_path is None or not os.path.exists(vid_path)):
        raise FileNotFoundError(f"Video path {vid_path} does not exist.")
    # ensure that vid_path is a path to valid .mp4 file 
    if not vid_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise ValueError(f"Invalid video file format: {vid_path}. Supported formats are .mp4, .avi, .mov, .mkv.")
    # continue to extraction phase 

    # create output dirs 
    out_dir = os.path.join(out_root, dir_name)
    os.makedirs(out_dir, exist_ok=True)
    # extract video raw
    cap = cv2.VideoCapture(vid_path)

    try:
        if not os.path.exists('data' + os.sep + dir_name):
            os.makedirs('data' + os.sep + dir_name)
    except OSError:
        print('Error: data output directory already exists. You may not rewrite existing video files.')
    
    # track frame
    curr_frame = 0
    frames = []
    while(True):
        # read frame
        check, frame = cap.read()

        if check:
            # store frame
            file = os.path.join(out_dir, f'frame_{curr_frame}.jpg')
            frames.append(file)
            cv2.imwrite(file, frame)
            curr_frame += 1
        else:
            break
