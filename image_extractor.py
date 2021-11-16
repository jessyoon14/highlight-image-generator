import cv2
import random


def generate_captioned_image():

def extract_image_from_range():

def add_text(image, text):


if __name__ == "__main__":
    # set up text constants
    font = cv2.FONT_HERSHEY_SIMPLEX

    vid = cv2.VideoCapture('samplevid.mp4')

    time_range = (1000, 2000) # in ms
    sentence = 'hello world'

    extract_time = random.randint(time_range[0], time_range[1])

    vid.set(cv2.CAP_PROP_POS_MSEC, extract_time)


    if (vid.isOpened()):
        ret, frame = vid.read()
        if ret == True:
            captioned_image = cv2.putText(frame, sentence, (50,100), font, 3, (255,255,255), 2, cv2.LINE_AA)
            cv2.imwrite('captured_image.jpg', frame)

    vid.release()
    cv2.destroyAllWindows()

