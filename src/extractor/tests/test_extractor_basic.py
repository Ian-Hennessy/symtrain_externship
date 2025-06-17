import os 
import pytest
from extractor.feature_parser import frame_extractor
from extractor.feature_parser import layout_extractor
from model import Parser
import cv2
import numpy as np


class DummyParser:
    def __init__(self, return_value):
        """
        return_value should be a list of dicts, 
        each with 'bbox' and maybe 'content'.
        """
        self._return = return_value

    def parse(self, _image_path):
        # Always return the same value to exercise extract_layout logic
        return self._return

@pytest.fixture
def dummy_png(tmp_path):
    """
    Create a 100×100 white PNG at tmp_path / 'dummy.png' and return its path.
    """
    img = 255 * np.ones((100, 100, 3), dtype=np.uint8)
    file_path = tmp_path / "dummy.png"
    cv2.imwrite(str(file_path), img)
    return str(file_path)


def test_no_elements_returns_empty(tmp_path, dummy_png):
    dir_path = tmp_path/"images"
    dir_path.mkdir()
    dest = dir_path/"images"
    os.rename(dummy_png, dest)

    results = frame_extractor.extract_frames(dir_path, dest)
    assert results == [], "Expected empty results for no elements"


def test_skips_invalid_files(tmp_path):
    dir_path = tmp_path/"mixed_data"
    dir_path.mkdir()

    # 1. write dummy png 
    img = 255* np.ones((50, 50, 3), dtype=np.uint8)
    dummy_png = dir_path/"keep.png"
    cv2.imwrite(str(dummy_png), img)
    out_path = dir_path/"keep_frames"
    # 2. write non-image file
    dummy_txt = dir_path/"skip.txt"
    with open(dummy_txt, "w") as f:
        f.write("This is a text file, not an image.")
    
    parser = DummyParser(return_val = [])
    frame_extractor.extract_frames(str(dir_path), out_path)
    results = os.listdir(str(out_path))
    assert len(results) == 1, "Only one valid image was in the directory"
  

def test_raises_error_on_unreadable_file(tmp_path):
    dir_path = tmp_path/"broken_dir"
    dir_path.mkdir()

    # Create a dummy PNG
    dummy_png = dir_path/"unreadable.png"
    dummy_png.write_bytes(b"") ## 0 byte file can't be read!!

    parser = DummyParser(return_val = [])

    with pytest.raises(FileNotFoundError):
        frame_extractor.extract_frames(str(dir_path), parser)
    
def test_writes_to_correct_dir(tmp_path, dummy_vid): 
    """
    Test to ensure correct directory written to when running extract_frames
    """
    dir_path = tmp_path/"test_frames_written_dir"
    dir_path.mkdir()

    # Create a dummy video file
    dummy_vid_path = dir_path/"test_video.mp4"
    cv2.VideoWriter(str(dummy_vid_path), cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480)).release()

    parser = DummyParser(return_val = [])

    # Run the frame extraction
    frame_extractor.extract_frames(str(dir_path), "test_video_frames")
    # output results as a list of the final directory contents 
    results = os.listdir(str(dir_path))
    
    # ensure frames are written and to the correct directory 
    assert len(results) > 0 
    assert all(file.endswith('.jpg') for file in results) or all(file.endswith('.png') for file in results), "All files should be image files, and the same kind"

def test_extract_correct_num_frames(tmp_path):
    """
    Test to ensure that the frame extractor correctly assigns one frame per second to video file, and outputs proper number 
    of images to the directory 
    """
    dir_path = tmp_path/"test_frame_count"
    dir_path.mkdir()

    # create dummy video, length will be 15 seconds 
    dummy_vid_path = dir_path
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(str(dummy_vid_path), fourcc, 1, (640, 480))

    for i in range(15):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        out.write(frame)
    out.release()
    
    # run frame extraction 
    frame_extractor.extract_frames(str(dummy_vid_path), 'test_num_frames_video')

    result = os.listdir(str(dir_path))

    assert (len(result) == 15), "Expected 15 frames to be extracted from 15-second video."

