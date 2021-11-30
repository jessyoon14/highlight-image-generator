from download import save_and_crop_youtube_video
import speech_to_text_fun
import capture_image

def run_end_to_end(youtube_link, start_time, end_time):
    # download video

    save_and_crop_youtube_video(youtube_link, start_time, end_time)

    # extract audio
    

    # separate audio
    # run STT
    audio1 = "AUDIO1_PATH"
    audio2 = "AUDIO2_PATH"
    script = speech_to_text_fun(audio1, audio2)
    # capture image
    video = "VIDEO_PATH"
    capture_image(video, script)

    # generate image zip file

