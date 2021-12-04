from .constants import VIDEO_DIR, AUDIO_DIR, AUDIO_RES_DIR, VV_DIR
import subprocess
import os

def use_model(vid_name):
    ### parameter :
    ###    - vid_name(str) : video name without extension. len(vid_name) == 5.
    
    os.chdir(VV_DIR)

    # change video to 25 fps
    vid_path = f'{VIDEO_DIR}/{vid_name}'

    command_convert = f'ffmpeg -i {vid_path}.mp4 -filter:v fps=fps=25 {vid_path}25fps.mp4'

    subprocess.Popen(
        command_convert, shell=True #, stdout=subprocess.DEVNULL
    ).communicate()

    print('finish converting video')
    command_move = f'mv {vid_path}25fps.mp4 {vid_path}.mp4'
    subprocess.Popen(
        command_move, shell=True #, stdout=subprocess.DEVNULL
    ).communicate()

    # face detection
    command_detect_face = f'python ./utils/detectFaces.py '\
                            f'--video_input_path {vid_path}.mp4 '\
                            f'--output_path {vid_path}/ '\
                            f'--number_of_speakers 2 '\
                            f'--scalar_face_detection 1.5 '\
                            f'--detect_every_N_frame 8'\

    subprocess.Popen(
        command_detect_face, shell=True
    ).communicate()

    # extract audio from video
    command_extract_audio = f'ffmpeg -i {vid_path}.mp4 -vn -ar 16000 -ac 1 -ab 192k -f wav {AUDIO_DIR}/{vid_name}.wav'
    subprocess.Popen(
        command_extract_audio, shell=True, stdout=subprocess.DEVNULL
    ).communicate()

    print('finish extract audio')

    # crop mouth from video
    command_crop_mouth = f'python ./utils/crop_mouth_from_video.py '\
                            f'--video-direc {vid_path}/faces/ '\
                            f'--landmark-direc {vid_path}/landmark/ '\
                            f'--save-direc {vid_path}/mouthroi/ '\
                            f'--convert-gray '\
                            f'--filename-path {vid_path}/filename_input/{vid_name}.csv'
    
    subprocess.Popen(
        command_crop_mouth, shell=True, stdout=subprocess.DEVNULL
    ).communicate()
    
    print('finish crop mouth')

    # run video testing
    command_run_video_test = f'python ./testRealVideo.py '\
                                f'--mouthroi_root {VIDEO_DIR}/{vid_name}/mouthroi/ '\
                                f'--facetrack_root {VIDEO_DIR}/{vid_name}/faces/ '\
                                f'--audio_path {AUDIO_DIR}/{vid_name}.wav '\
                                f'--weights_lipreadingnet ./pretrained_models/lipreading_best.pth '\
                                f'--weights_facial ./pretrained_models/facial_best.pth '\
                                f'--weights_unet ./pretrained_models/unet_best.pth '\
                                f'--weights_vocal ./pretrained_models/vocal_best.pth '\
                                f'--lipreading_config_path ./configs/lrw_snv1x_tcn2x.json '\
                                f'--num_frames 64 '\
                                f'--audio_length 2.55 '\
                                f'--hop_size 160 '\
                                f'--window_size 400 '\
                                f'--n_fft 512 '\
                                f'--unet_output_nc 2 '\
                                f'--normalization '\
                                f'--visual_feature_type both '\
                                f'--identity_feature_dim 128 '\
                                f'--audioVisual_feature_dim 1152 '\
                                f'--visual_pool maxpool '\
                                f'--audio_pool maxpool '\
                                f'--compression_type none '\
                                f'--reliable_face '\
                                f'--audio_normalization '\
                                f'--desired_rms 0.7 '\
                                f'--number_of_speakers 2 '\
                                f'--mask_clip_threshold 5 '\
                                f'--hop_length 2.55 '\
                                f'--lipreading_extract_feature '\
                                f'--number_of_identity_frames 1 '\
                                f'--output_dir_root {AUDIO_RES_DIR}/{vid_name}/'

    subprocess.Popen(
        command_run_video_test, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ).communicate()


    audio_file_1 = f'{AUDIO_RES_DIR}/{vid_name}/speaker1.wav'
    audio_file_2 = f'{AUDIO_RES_DIR}/{vid_name}/speaker2.wav'
    
    print('finish extracting 2 speaker audio files')

    return (audio_file_1, audio_file_2)

if __name__=="__main__":
    use_model(AUDIO_DIR + "/FRSmw_final.wav")