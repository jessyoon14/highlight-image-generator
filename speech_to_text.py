import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

import os
SPEECH_KEY = os.environ.get("SPEECH_KEY")
REGION = os.environ.get("REGION")

def from_file():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY,
                                           region=REGION)
    audio_input = speechsdk.AudioConfig(filename="./sample.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    result = speech_recognizer.recognize_once_async().get()
    print(result.text)


if __name__ == "__main__":
    from_file()