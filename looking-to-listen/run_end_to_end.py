# from local import VIDEO_DIR, AUDIO_DIR
# from local.loader.constants import EMBED_DIR
from local.loader import download, extract_audio, generate_video_embedding
from run_model import run_model
from argparse import ArgumentParser, Namespace
from pathlib import Path
from asteroid.utils import parse_args_as_dict, prepare_parser_from_dict
import csv
import yaml

if __name__=="__main__":

    # download video
    video_link = "https://www.youtube.com/watch?v=5clkKQ6f4FI"
    start_time = 7
    end_time = 11

    VIDEO_DIR = "./storage_dir/storage/video"
    AUDIO_DIR = "./storage_dir/storage/audio"
    EMBED_DIR = "./storage_dir/storage/embed"

    # args = argparser.parse_args(["--jobs", 1, "--video_link", video_link, "--start_time", start_time, "--end_time", end_time, "--vid_dir", vid_dir])
    args1 = Namespace(jobs=1, video_link=video_link, start_time=start_time, end_time=end_time, vid_dir=VIDEO_DIR)
    download.main(args1)
    
    # extract audio
    # args = argparser.parse_args(["--jobs", 2, "--aud-dir", AUDIO_DIR, "--vid-dir", VIDEO_DIR, "--sampling-rate", 16_000, "--audio-channel", 2, "--audio-extension", "wav", "--duration", 3])
    args2 = Namespace(jobs=2, aud_dir=AUDIO_DIR, vid_dir=VIDEO_DIR, sampling_rate=16_000, audio_channel=2, audio_extension="wav", duration=3)
    extract_audio.main(args2)
    
    # embed human faces
    path = Path(EMBED_DIR)
    video_path  = Path(f"{VIDEO_DIR}/{video_link[-5:]}_0_0_final.mp4")
    fake_video_path1 = Path(f"{VIDEO_DIR}/{video_link[-5:]}_0_0_final_face1.mp4")
    fake_video_path2 = Path(f"{VIDEO_DIR}/{video_link[-5:]}_0_0_final_face2.mp4")
    audio_path  = Path(f"{AUDIO_DIR}/{video_link[-5:]}_0_0_final_part0.wav")
        
    argparser = ArgumentParser()    
    args3 = Namespace(embed_dir=path, cuda=True, video_path=video_path, use_half=False)
  
    
    generate_video_embedding.main(args3)

    f = open('/home/irslab/ws/highlight-image-generator/looking-to-listen/'+'val.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(['video_1','video_2','audio_1','audio_2','mixed_audio'])
    wr.writerow([fake_video_path1, fake_video_path2, audio_path, audio_path, audio_path])
    f.close()

    # run model
    # EXP_DIR = '/home/irslab/ws/highlight-image-generator/looking-to-listen/exp'
    EXP_DIR = './exp'
    # args4 = Namespace(gpus=-1, n_src=2, exp_dir=EXP_DIR)

    parser = ArgumentParser()
    parser.add_argument("--gpus", type=str, help="list of GPUs", default="-1")
    parser.add_argument(
        "--n-src",
        type=int,
        help="number of inputs to neural network",
        default=2,
    )
    parser.add_argument(
        "--exp_dir",
        default=EXP_DIR,
        help="Full path to save best validation model",
    )

    with open("local/conf.yml") as f:
        def_conf = yaml.safe_load(f)
    parser = prepare_parser_from_dict(def_conf, parser=parser)

    arg_dic, plain_args = parse_args_as_dict(parser, return_plain_args=True)
    print(arg_dic)
    run_model.main(arg_dic)


