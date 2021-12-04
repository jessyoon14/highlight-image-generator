import cv2
import random
import os
import numpy as np
import shutil
from .constants import IMAGE_RES_DIR

# font settings
FONT = cv2.FONT_HERSHEY_SIMPLEX
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SCALE = 1
FONT_THICKNESS = 2
POSITION = (100, 100)
LINE_TYPE = cv2.LINE_AA


def generate_captioned_image(video, start_time, end_time, sentence):
    image = extract_image_from_range(video, start_time, end_time)
    captioned_image = add_text(image, sentence)
    return captioned_image


def extract_image_from_range(video, start_time, end_time):
    extract_time = random.randint(start_time, end_time)
    video.set(cv2.CAP_PROP_POS_MSEC, extract_time // 10000) 
    if (video.isOpened()):
        ret, frame = video.read()
        if ret == True:
            return frame
        else: 
            print("ERROR ON FRAME READING")
    else:
        print('ERROR ON video.isOpened()')
    return None


def add_text(image, text):
    height, width, _ = image.shape
    pos = (20, height - 20,)
    return cv2.putText(image, text, pos, FONT, FONT_SCALE, WHITE, FONT_THICKNESS, LINE_TYPE, False)

def capture_image(video_path, script):
    print('script: ', script)
    # video_path = video_path
    video_name = video_path.split('/')[-1].split('.')[-2] 
        
    # read video from file
    if os.path.isfile(video_path):
        video = cv2.VideoCapture(video_path)
    else:
        print("fail")
        
    # read video from YouTube (더 오래 걸리지만, 영상을 다운 받을 수 없다면 사용 가능)
    #
    # url = 'https://www.youtube.com/watch?v=IZIywuXTmJk&ab_channel=%EB%94%A9%EA%B3%A0%EB%AE%A4%EC%A7%81%2Fdingomusic'
    # youtube_video = pafy.new(url)
    # best_resolution_video = youtube_video.getbest(preftype='mp4')
    # video = cv2.VideoCapture(best_resolution_video.url)
    # script = [{
    #     'start_time': 1000,
    #     'end_time': 2000,
    #     'sentence': [(1, "hello world"), (2, "hello human")]
    # }, {
    #     'start_time': 4000,
    #     'end_time': 6000,
    #     'sentence': [(1, "hello world"), (2, "hello human")]
    # },{
    #     'start_time': 8000,
    #     'end_time': 10000,
    #     'sentence': [(1, "hello world"), (2, "hello human")]
    # }]

    # sentences = input['sentence']
    # start_time = input['start_time']
    # end_time = input['end_time']
    # IMAGE_RES_DIR = os.getcwd() + '/media/image_result'
    save_dir = f'{IMAGE_RES_DIR}/{video_name}'
    if os.path.isdir(save_dir):
        # if remove:
        shutil.rmtree(save_dir)
    # else:
    #         # return
    os.makedirs(save_dir)


    for i, elem in enumerate(script):

        sentences = elem['sentence']
        start_time = elem['start_time']
        end_time = elem['end_time']
        
        image = extract_image_from_range(video, start_time, end_time)

        height, width, _ = image.shape
        position1 = (20, height - 20)
        position2 = (20, 30)

        # frame = cv2.resize(image, (height, width))
        # bg_color = (0,0,0)
        # bg = np.full((frame.shape), bg_color, dtype=np.uint8)

        # write first sentence
        i = 0
        script1 = sentences[i][1]
        prev_talker = sentences[i][0]
        curr_talker = None if len(sentences) == 1 else sentences[i+1][0]
        
        while prev_talker == curr_talker:
            script1 = script1 + sentences[i+1][1]
            
            i+=1
            prev_talker = sentences[i][0]
            curr_talker = None if len(sentences) == 1 else sentences[i+1][0]
        
        pos = position1 if sentences[0][0] == 1 else position2
        captioned_image = cv2.putText(image, script1, pos, FONT, FONT_SCALE, WHITE, FONT_THICKNESS, LINE_TYPE, False)
        #captioned_image = cv2.putText(image, sentences[0][1], pos, FONT, FONT_SCALE, WHITE, FONT_THICKNESS, LINE_TYPE, False)
        #captioned_image = cv2.putText(bg, sentences[0][1], pos, FONT, FONT_SCALE, WHITE, FONT_THICKNESS, LINE_TYPE, False)
        # write second sentence
        if len(sentences) > i:
            pos = position1 if sentences[i][0] == 1 else position2
            
            script2 = sentences[i][1]
            prev_talker = sentences[i][0]
            curr_talker = None if len(sentences) == 1 else sentences[i+1][0]
            
            while prev_talker == curr_talker:
                script2 = script2 + sentences[i+1][1]
            
                i+=1
                prev_talker = sentences[i][0]
                curr_talker = None if len(sentences) == 1 else sentences[i+1][0]
            
            
            captioned_image = cv2.putText(image, script2, pos, FONT, FONT_SCALE, WHITE, FONT_THICKNESS, LINE_TYPE, False)
            #captioned_image = cv2.putText(bg, sentences[1][1], pos, FONT, FONT_SCALE, WHITE, FONT_THICKNESS, LINE_TYPE, False)

        # x, y, w, h = cv2.boundingRect(bg[:,:,2])
        # w, h = w+10, h+10
        # x, y = x-5, y-5
        # result = frame.copy()
        # result[y:y+h, x:x+w] = bg[y:y+h, x:x+w]

        cv2.imwrite(f'{save_dir}/captured_image{i}.jpg', image)
        #cv2.imwrite(f'{save_dir}/captured_image{i}.jpg', frame)


    video.release()

if __name__ == "__main__":
    video_path = './media/video/P8yBk_final.mp4'

    input = {
        'start_time': 1,
        'end_time': 2,
        'sentence': [(1, "hello world"), (2, "hello human")]
    }

    capture_image(video_path,input)
