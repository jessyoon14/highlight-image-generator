

def face_detect(video_path):
    # download video

    video_path = #TODO
    
    save_and_crop_youtube_video(youtube_link, start_time, end_time)

    # extract audio
        args, path = arg_path
    name = path.stem
    dir_name = path.parents[0]
    audio_dir = args.aud_dir
    audio_path = os.path.join(audio_dir, name)
    print(audio_path)
    extract_audio(video_path, output_audio_path)
    

    # separate audio
    # run STT
    audio1 = "AUDIO1_PATH"
    audio2 = "AUDIO2_PATH"
    script = speech_to_text_fun(audio1, audio2)
    # capture image
    video = "VIDEO_PATH"
    capture_image(video, script)

    # generate image zip file
    
