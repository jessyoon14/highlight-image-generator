from .download import save_and_crop_youtube_video
from .speech_to_text import speech_to_text_fun
from .seperator import use_model
from .image_extractor import capture_image

# https://www.youtube.com/watch?v=mwOB_pVNI1c

def run_end_to_end(youtube_link, start_time, end_time):

    file_name = youtube_link[-5:] + "_final"
    # # download video    
    video_path = save_and_crop_youtube_video(youtube_link, start_time, end_time)
    
    # separate audio
    print('start use_model')
    result_paths = use_model(file_name)
    print('finish use_model')

    # run STT
    audio1 = result_paths[0]
    audio2 = result_paths[1]
    
    ### audio1 = "/home/yominx/ws/highlight-image-generator/media/audio_result/P8yBk_final/speaker1.wav"
    ### audio2 = "/home/yominx/ws/highlight-image-generator/media/audio_result/P8yBk_final/speaker2.wav"

    # temp
    # video_path = "/home/yominx/ws/highlight-image-generator/media/video/y3Pss_final.mp4"
    # result_paths = ["/home/yominx/ws/highlight-image-generator/media/audio_result/y3Pss_final/speaker1.wav", "/home/yominx/ws/highlight-image-generator/media/audio_result/y3Pss_final/speaker2.wav"]
    # audio1 = result_paths[0]
    # audio2 = result_paths[1]

    print('start speech to text')
    script = speech_to_text_fun(audio1, audio2)
    print('finish speech to text')
    # # capture image
    # # video = "/home/yominx/ws/highlight-image-generator/media/video/video_tracked1.mp4"
    # print(video_path)
    # video_path = "/home/yominx/ws/highlight-image-generator/media/video/P8yBk_final.mp4"
    capture_image(video_path, script)

    # # # generate image zip file

if __name__=="__main__":
    print('Start run_end_to_end')
    
    run_end_to_end('https://youtu.be/V7g2HSy3Pss', 275, 285)
    # run_end_to_end('https://www.youtube.com/watch?v=QuIQ_RhVuCs', 0, 10)
    print('finish run_end_to_end')