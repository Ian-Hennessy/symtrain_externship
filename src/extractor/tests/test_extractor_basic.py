import os
import cv2
import numpy as np
import pytest
from extractor.feature_parser.frame_extractor import extract_frames

@pytest.fixture
def dummy_video(tmp_path):
    path = tmp_path / "video.mp4"
    h, w = 100, 200
    out = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), 1, (w,h))
    # 3 frames of solid black
    for _ in range(3):
        out.write(np.zeros((h, w, 3), dtype=np.uint8))
    out.release()
    return str(path)

def test_extract_three_frames(tmp_path, dummy_video):
    out_root = tmp_path / "data"
    frames = extract_frames(dummy_video, "out1", out_root=str(out_root), fps=1)
    assert len(frames) == 3
    # ensure files exist on disk
    for f in frames:
        assert os.path.exists(f)
        assert f.endswith(".jpg")

def test_nonexistent_path_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_frames(str(tmp_path/"nope.mp4"), "x", out_root=str(tmp_path/"data"))

def test_bad_extension_raises(tmp_path):
    bad = tmp_path / "foo.txt"
    bad.write_text("not a video")
    with pytest.raises(ValueError):
        extract_frames(str(bad), "x", out_root=str(tmp_path/"data"))


