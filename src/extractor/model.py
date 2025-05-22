"""
Creation and training of new LayoutParser model 
to detect and segment UI elements in still frames 
of UI demos 
"""
import os
import json
import cv2
import numpy as np
import torch
import layoutparser as lp