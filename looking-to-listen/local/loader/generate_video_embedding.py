import cv2
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from asteroid.data.avspeech_dataset import get_frames
from facenet_pytorch import MTCNN, InceptionResnetV1, extract_face

from .frames import input_face_embeddings
from .constants import VIDEO_DIR, EMBED_DIR

FRAMES = 75


def store_corrupt(path):
    with open(args.corrupt_file, "a") as f:
        f.write(path.as_posix() + "\n")


def cache_embed(path, mtcnn, resnet, args):
    orig_path = path
    if not path.is_file():
        path = "../.." / path
    video_file_name = path.stem.split("_")

    if len(video_file_name) < 3:
        store_corrupt(orig_path)
        return

    try:
        pos_x, pos_y = (
            int(video_file_name[-3]) / 10000,
            int(video_file_name[-2]) / 10000,
        )
    except ValueError as e:
        print(str(e))
        store_corrupt(orig_path)
        return

    video_buffer = get_frames(cv2.VideoCapture(path.as_posix()))
    total_frames = video_buffer.shape[0]

    video_parts = total_frames // FRAMES  # (25fps * 3)

    embeddings = []
    for part in tqdm(range(video_parts)):
        # frame_name = path.stem + f"1_part{part}"
        embed_path1 = Path(args.embed_dir, path.stem + f"_face1_part{part}" + ".npy")
        embed_path2 = Path(args.embed_dir, path.stem + f"_face2_part{part}" + ".npy")
        
        if embed_path1.is_file() and embed_path2.is_file():
            continue
        raw_frames = video_buffer[part * FRAMES : (part + 1) * FRAMES]

        (embed1, embed2) = input_face_embeddings(
            raw_frames,
            is_path=False,
            mtcnn=mtcnn,
            resnet=resnet,
            face_embed_cuda=args.cuda,
            use_half=args.use_half,
            coord=[pos_x, pos_y],
        )

        if (embed1 is None) or (embed2 is None):
            # store_corrupt(orig_path)
            print("Corrupt", path)
            return

        embeddings.append((embed1, embed_path1))
        embeddings.append((embed2, embed_path2))

    # save if all parts are not corrupted
    for embed, embed_path in embeddings:
        np.save(embed_path, embed.cpu().numpy())


def main(args):

    if args.cuda and torch.cuda.is_available():
        device = torch.device("cuda:0")
    else:
        device = torch.device("cpu")

    mtcnn = MTCNN(keep_all=True).eval().to(device)
    mtcnn.device = device

    resnet = InceptionResnetV1(pretrained="vggface2").eval().to(device)

    # get_video takes 1 arg: video path
    video_path = [args.video_path]

    print(f"Total embeddings: {len(video_path)}")
    for path in tqdm(video_path, total=len(video_path)):
        cache_embed(Path(path), mtcnn, resnet, args)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--embed-dir", default=Path(EMBED_DIR), type=Path)
    parser.add_argument("--cuda", dest="cuda", action="store_true", default=False)
    parser.add_argument("--video-path", default=Path("../../storage_dir/storage/video/v5qLA_0_0_final.mp4"), type=Path)
    # parser.add_argument("--video-path", default=Path("../../storage_dir/storage/video/6f4FI_0_0_final.mp4"), type=Path)
    # parser.add_argument("--audio-path", default=Path("../../storage_dir/storage/audio/6f4FI_0_0_final_part0.wav"), type=Path)
    parser.add_argument("--use-half", dest="use_half", action="store_true", default=False)

    args = parser.parse_args()

    main(args)
