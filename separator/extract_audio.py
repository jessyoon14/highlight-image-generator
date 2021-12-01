import os
import cv2
import time
import argparse
import subprocess
import pandas as pd
from pathlib import Path
import concurrent.futures
from tqdm import tqdm

from constants import AUDIO_DIR

SAMPLING_RATE = 16_000
AUDIO_CHANNEL = 2
AUDIO_EXTENTION = "wav"
DURATION = 3


def extract_audio(video_path):
    video_path = Path(video_path)
    video_file_name = video_path.stem
    output_audio_path = os.path.join(AUDIO_DIR, video_file_name) + '.wav' 
    video = cv2.VideoCapture(Path(video_path).as_posix())

    command = (
            f"ffmpeg -y -i {video_path.as_posix()} -f {AUDIO_EXTENTION} -ab 64000 "
            f"-vn -ar {SAMPLING_RATE} -ac {AUDIO_CHANNEL} - | sox -t "
            f"{AUDIO_EXTENTION} - -r 16000 -c 1 -b 8 "
            f"{output_audio_path}"
        )

    subprocess.Popen(
        command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ).communicate()

    return output_audio_path

if __name__== "__main__":
    print('start extract_audio')
    extract_audio('../media/video/FRSmw_final.mp4')
    print('finish extract_audio')