import cv2
import random
import os
import numpy as np
import shutil
from .constants import IMAGE_RES_DIR
import pyshine as ps

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

def get_x_position(speaker, image_width):
    
    if speaker == 1:
        return 40
    else:
        return image_width // 2



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

    max_line_len = 38

    # preprocess
    for elem in script:     
        sentences = elem['sentence']
        for i, sentence in enumerate(sentences):
            speaker = sentence[0]
            text = sentence[1]
            if len(text) > max_line_len:
                cut_index = text.find(' ', max_line_len)
                sentences[i] = (speaker, text[:cut_index])
                sentences.insert(i+1, (speaker, text[cut_index:]))


    for i, elem in enumerate(script):

        sentences = elem['sentence']
        start_time = elem['start_time']
        end_time = elem['end_time']
        
        image = extract_image_from_range(video, start_time, end_time)

        height, width, _ = image.shape
        position1 = (40, height - 200)
        position2 = (40, height - 150)
        position3 = (40, height - 100)
        position4 = (40, height - 50)

        
        # pos = position1 if sentences[0][0] == 1 else position2

        speaker1 = sentences[0][0]

        text = sentences[0][1]

        # cv2.putText(img=image, text=text, org=(get_x_position(speaker1, width), position1[1]),
        #             fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=1, color=[0, 0, 0], lineType=cv2.LINE_AA, thickness=6)
        # cv2.putText(img=image, text=text, org=(get_x_position(speaker1, width), position1[1]),
        #             fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=1, color=[255, 255, 255], lineType=cv2.LINE_AA, thickness=2)
        image = ps.putBText(image, text,text_offset_x=get_x_position(speaker1, width),text_offset_y=position1[1],vspace=10,hspace=10, font_scale=1.0,background_RGB=(0,0,0),text_RGB=(255,250,250))

        # if simultaneous speaker
        if len(sentences) > 1:
            speaker2 = sentences[1][0]
            text2 = sentences[1][1]
            # cv2.putText(img=image, text=text2, org=(get_x_position(speaker2, width), position2[1]),
            #             fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=1, color=[0, 0, 0], lineType=cv2.LINE_AA, thickness=6)
            # cv2.putText(img=image, text=text2, org=(get_x_position(speaker2, width), position2[1]),
            #             fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=1, color=[255, 255, 255], lineType=cv2.LINE_AA, thickness=2)
            # cv2.putText(im, "Test", (0,size[1]), cv2.FONT_HERSHEY_COMPLEX, 2, (0,), 4)
            # cv2.putText(im, "Test", (0,size[1]), cv2.FONT_HERSHEY_COMPLEX, 2, (255,), 2)
            image = ps.putBText(image, text2,text_offset_x=get_x_position(speaker2, width),text_offset_y=position2[1],vspace=10,hspace=10, font_scale=1.0,background_RGB=(0,0,0),text_RGB=(255,250,250))

            if len(sentences) > 2:
                speaker3 = sentences[2][0]
                text3 = sentences[2][1]
                # cv2.putText(img=image, text=text3, org=(get_x_position(speaker3, width), position3[1]),
                #             fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=1, color=[0, 0, 0], lineType=cv2.LINE_AA, thickness=6)
                # cv2.putText(img=image, text=text3, org=(get_x_position(speaker3, width), position3[1]),
                #             fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=1, color=[255, 255, 255], lineType=cv2.LINE_AA, thickness=2)
                image = ps.putBText(image, text3,text_offset_x=get_x_position(speaker3, width),text_offset_y=position3[1],vspace=10,hspace=10, font_scale=1.0,background_RGB=(0,0,0),text_RGB=(255,250,250))
                
                if len(sentences) > 3:
                    speaker4 = sentences[3][0]
                    text4 = sentences[3][1]
                    # cv2.putText(img=image, text=text4, org=(get_x_position(speaker4, width), position4[1]),
                    #             fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=1, color=[0, 0, 0], lineType=cv2.LINE_AA, thickness=6)
                    # cv2.putText(img=image, text=text4, org=(get_x_position(speaker4, width), position4[1]),
                    #             fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=1, color=[255, 255, 255], lineType=cv2.LINE_AA, thickness=2)
                    image = ps.putBText(image, text4,text_offset_x=get_x_position(speaker4, width),text_offset_y=position4[1],vspace=10,hspace=10, font_scale=1.0,background_RGB=(0,0,0),text_RGB=(255,250,250))



        # write second sentence
        # if len(sentences) > 1:
        #     pos = position1 if sentences[1][0] == 1 else position2
            
            # script2 = sentences[i][1]
            # prev_talker = sentences[i][0]
            # curr_talker = None if len(sentences) == 1 else sentences[i+1][0]
            
            # while prev_talker == curr_talker:
            #     script2 = script2 + sentences[i+1][1]
            
            #     i+=1
            #     prev_talker = sentences[i][0]
            #     curr_talker = None if len(sentences) == 1 else sentences[i+1][0]
            
            
            # captioned_image   = ps.putBText(image, sentences[1][1],text_offset_x=pos[0],text_offset_y=pos[1],vspace=10,hspace=10, font_scale=1.0,background_RGB=(0,0,0),text_RGB=(255,250,250))

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
