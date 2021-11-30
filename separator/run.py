from download import save_and_crop_youtube_video
import speech_to_text_fun

def run_end_to_end(youtube_link, start_time, end_time):
    # download video
    save_and_crop_youtube_video(youtube_link, start_time, end_time)

    # extract audio
    

    # separate audio
    # run STT
    audio1 = ""
    audio2 = ""
    script = speech_to_text_fun(audio1, audio2)

    # capture image
    

    # generate image zip file

