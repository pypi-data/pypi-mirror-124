"""
This module contains helper functions to manipulate videos 

@authors: Gergo Turi gt2253@cumc.columbia.edu
"""

import cv2

def get_fps(vid_path):
    """
    retrieves acqusition rate from AVI video.

    Parameters:
    ===========
    vid_path: str
        path to the video
    """
    
    video = cv2.VideoCapture(video_file)
    fps = video.get(cv2.CAP_PROP_FPS)
    print(f'fps is {fps}')
    return fps


