from download import save_and_crop_youtube_video
from extract_audio import extract_audio
from speech_to_text import speech_to_text_fun
from seperator import use_model
from image_extractor import capture_image

# https://www.youtube.com/watch?v=mwOB_pVNI1c

def run_end_to_end(youtube_link, start_time, end_time):

    file_name = youtube_link[-5:] + "_final"
    # download video    
    video_path = save_and_crop_youtube_video(youtube_link, start_time, end_time)
    
    # separate audio
    print('start use_model')
    result_paths = use_model(file_name)
    print('finish use_model')

    # # # run STT
    # audio1 = result_paths[0]
    # audio2 = result_paths[1]
    # # audio1 = "/home/yominx/ws/highlight-image-generator/media/audio_result/speaker1.wav"
    # # audio2 = "/home/yominx/ws/highlight-image-generator/media/audio_result/speaker2.wav"
    # script = speech_to_text_fun(audio1, audio2)

    # # capture image
    # # video = "/home/yominx/ws/highlight-image-generator/media/video/video_tracked1.mp4"
    # capture_image(video_path, script)

    # # # generate image zip file

if __name__=="__main__":
    print('Start run_end_to_end')
    
    run_end_to_end('https://www.youtube.com/watch?v=5rXha4P8yBk', 100, 120)
    # run_end_to_end('https://www.youtube.com/watch?v=QuIQ_RhVuCs', 0, 10)
    print('finish run_end_to_end')