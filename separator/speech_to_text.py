import os
import time
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

SPEECH_KEY = os.environ.get("SPEECH_KEY")
REGION = os.environ.get("REGION")


def from_file(p_num, file_path):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY,
                                           region=REGION)

    speech_config.request_word_level_timestamps()
    speech_config.output_format = speechsdk.OutputFormat(1)
    audio_input = speechsdk.AudioConfig(filename=file_path)
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

    transcript_display_list = []
    transcript_ITN_list = []
    confidence_list = []
    words = []

    def parse_azure_result(evt):
        import json
        response = json.loads(evt.result.json)
        transcript_display_list.append(response['DisplayText'])
        confidence_list_temp = [item.get('Confidence') for item in response['NBest']]
        max_confidence_index = confidence_list_temp.index(max(confidence_list_temp))
        confidence_list.append(response['NBest'][max_confidence_index]['Confidence'])
        transcript_ITN_list.append(response['NBest'][max_confidence_index]['ITN'])
        words.append(response['NBest'][max_confidence_index]['Words'])
        # logger.debug(evt)

    # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    # speech_recognizer.recognized.connect(lambda evt: print(f'RECOGNIZED: {format(evt)}, {json.loads(evt.result.json)}'))
    speech_recognizer.recognized.connect(parse_azure_result)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)

    print(transcript_display_list)
    print(transcript_ITN_list)
    print(confidence_list)
    print(words)

    list_of_sentence = []

    for i in range(len(transcript_display_list)):
        start_time = words[i][0]['Offset']
        end_time = words[i][-1]['Offset'] + words[i][-1]['Duration']
        list_of_sentence.append(((start_time, end_time), p_num, transcript_display_list[i]))

    return list_of_sentence


def make_script(sentences, transcript, d, min=3e+7, max=5e+7):
    if len(sentences) > 1:
        if sentences[0][0][1] < sentences[1][0][0]:
            # d['end_time'] = sentences[0][0][1] if d['end_time'] < sentences[0][0][1] else d['end_time']
            d['sentence'].append((sentences[0][1], sentences[0][2]))
            transcript.append(d)
            sentences.pop(0)
            return make_script(sentences, transcript,
                               {'start_time': sentences[0][0][0], 'end_time': sentences[0][0][1], 'sentence': []})
        else:
            d['end_time'] = sentences[0][0][1] if d['end_time'] < sentences[0][0][1] else d['end_time']
            d['sentence'].append((sentences[0][1], sentences[0][2]))
            sentences.pop(0)
            return make_script(sentences, transcript, d)
    else:
        d['end_time'] = sentences[0][0][1]
        d['sentence'].append((sentences[0][1], sentences[0][2]))
        transcript.append(d)
        return transcript

def speech_to_text_fun(audio1, audio2):
    p1, p2 = 1, 2
    s1 = from_file(p1, audio1)
    s2 = from_file(p2, audio2)

    sentences = s1 + s2
    sentences.sort(key=lambda x: (x[0][0]))  # sort by start time
    print(sentences)

    empty_script = []

    script = make_script(sentences, empty_script,
                         {'start_time': sentences[0][0][0], 'end_time': sentences[0][0][1], 'sentence': []})

    return script


if __name__ == "__main__":
    p1, p2 = 1, 2
    s1 = from_file(p1, "./pause.wav")
    s2 = from_file(p2, "./sample2.wav")

    sentences = s1 + s2
    sentences.sort(key=lambda x: (x[0][0]))  # sort by start time
    print(sentences)

    empty_script = []

    script = make_script(sentences, empty_script,
                         {'start_time': sentences[0][0][0], 'end_time': sentences[0][0][1], 'sentence': []})

    print(script)
