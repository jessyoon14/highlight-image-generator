import cv2
import random
import pafy

# font settings
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_COLOR = (255, 255, 255)
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
    video.set(cv2.CAP_PROP_POS_MSEC, extract_time)
    if (video.isOpened()):
        ret, frame = video.read()
        if ret == True:
            return frame

    return None


def add_text(image, text):
    height, width, _ = image.shape
    pos = (20, height - 20,)
    return cv2.putText(image, text, pos, FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS, LINE_TYPE, False)


if __name__ == "__main__":
    video_path = 'samplevid.mp4'
    start_time = 1000
    end_time = 2000
    sentence = 'hello world'

    # read video from file
    video = cv2.VideoCapture(video_path)

    # read video from YouTube (더 오래 걸리지만, 영상을 다운 받을 수 없다면 사용 가능)
    #
    # url = 'https://www.youtube.com/watch?v=IZIywuXTmJk&ab_channel=%EB%94%A9%EA%B3%A0%EB%AE%A4%EC%A7%81%2Fdingomusic'
    # youtube_video = pafy.new(url)
    # best_resolution_video = youtube_video.getbest(preftype='mp4')
    # video = cv2.VideoCapture(best_resolution_video.url)

    image = generate_captioned_image(video, start_time, end_time, sentence)

    cv2.imwrite('captured_image.jpg', image)