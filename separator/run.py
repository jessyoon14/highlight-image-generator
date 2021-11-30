from download import save_and_crop_youtube_video
import speech_to_text_fun
import capture_image

def run_end_to_end(youtube_link, start_time, end_time):
    # download video    
    video_path = save_and_crop_youtube_video(youtube_link, start_time, end_time)

    # extract audio
    audio_path = extract_audio(video_path, output_audio_path)
    
    # separate audio
    result_paths = use_model(audio_path)

    # run STT
    audio1 = result_paths[0]
    audio2 = result_paths[1]
    script = speech_to_text_fun(audio1, audio2)
    
    # capture image
    video = "VIDEO_PATH"
    capture_image(video, script)

    # generate image zip file

    
