import os
import time
import tqdm
import argparse
import subprocess
import pandas as pd
from pathlib import Path
import concurrent.futures
from .constants import VIDEO_DIR


def download(link, path, final_name=None):
    command = "python -m yt_dlp {} --no-check-certificate --output {}.mp4 -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'"
    if os.path.exists(path) and os.path.isfile(path):
        print("File already downloaded")
        return False
    if final_name is not None and os.path.isfile(final_name):
        print("File already cropped")
        return True

    p = subprocess.Popen(
        command.format(link, path),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    return False


def crop(path, start, end, downloaded_name):
    # command = (
    #     "ffmpeg -y -i {}.mp4 -ss {} -t {} -pix_fmt yuv420p "
    #     "-c:a aac -b:a 128k -strict experimental -r 25 {}"
    # )
    command = (
        "ffmpeg -y -i {}.mp4 -ss {} -t {} -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p "
        "-c:a aac -b:a 128k -strict experimental -r 25 {}"
    )
    start_minute, start_second  = int(start // 60), int(start % 60)
    end_minute, end_second      = int((end - start) // 60), int((end - start) % 60) # int(end // 60) - start_minute, int(end % 60) - start_second

    new_filepath = downloaded_name + "_final.mp4"

    if os.path.exists(new_filepath) and os.path.isfile(new_filepath):
        return

    command = command.format(
        downloaded_name,
        f"{start_minute}:{start_second}",
        f"{end_minute}:{end_second}",
        new_filepath,
    )
    subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()

    remove_orig_file = f"rm -f {downloaded_name}.mp4"
    subprocess.Popen(
        remove_orig_file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()


def save_and_crop_youtube_video(youtube_link, start_time, end_time)
    path = Path(os.path.join(VIDEO_DIR, link[-5:]))
    downloaded_name = path.as_posix()
    cropped = download(link, downloaded_name, final_name=downloaded_name + "_final.mp4")
    if not cropped:
        crop(path, start, end, downloaded_name)
