import time
import json
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

import os
SPEECH_KEY = os.environ.get("SPEECH_KEY")
REGION = os.environ.get("REGION")

def from_file():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY,
                                           region=REGION)

    speech_config.request_word_level_timestamps()
    speech_config.output_format = speechsdk.OutputFormat(1)
    audio_input = speechsdk.AudioConfig(filename="./pause.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    # run single-shot
    # result = speech_recognizer.recognize_once_async().get()
    # print(result.json)

    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print(f'RECOGNIZED: {format(evt)}, {json.loads(evt.result.json)}'))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)


if __name__ == "__main__":
    from_file()