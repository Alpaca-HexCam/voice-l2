
from server import app
from flask import request, jsonify
import speech_recognition as sr
import os
import words2num
import re
from googletrans import Translator

import firebase
import firebase_admin
from firebase_admin import credentials, db, firestore, storage

firebase_admin.initialize_app()
db = firestore.client()
storage = firebase_admin.storage.bucket("gs://alpaca-72130.appspot.com")

@app.route('/')
@app.route('/index') #www.alapaca.com/index
def index():
    all_files = storage.child("audio_recordings").list_files()

    return all_files

@app.route('/create-document')
def create_document():
    try:
        db.collection(u'docs').add({'myfirst':'doc'})
        return "Completed request"
    except Exception as e:
        print(e)
        return 'Could not make request'


def speechToText(audio_file, lang):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:

        audio_text = r.listen(source)

        try:
            # using google speech recognition
            text = r.recognize_google(audio_text, language=lang)
            return text

        except:
            return None


def playAudio(audio_file):
    pygame.mixer.init()
    my_sound = pygame.mixer.Sound(audio_file)
    my_sound.play()
    pygame.time.wait(int(my_sound.get_length() * 1000))


def processSpeech(audio_file, type, lang="en-GB"):
    # Type is one of ["income", "expense", "general"]
    if type == "income":
        sign = 1
    elif type == "expense":
        sign = -1
    else:
        return None

    text = speechToText(audio_file, lang)
    if text is None:
        return None

    if not lang == "en-GB":
        translator = Translator()
        text = translator.translate(text, src=lang[:2], dest="en").text

    if text is None:
        return None

    words = text.split()

    print(words)

    val = 0
    for w in words:
        w = re.sub('[$£]', '', w)
        try:
            if w.isdigit():
                val += float(w)
            else:
                val += words2num.words2num(w)
        except:
            pass

    print(val)
    # numbers = [num for num in words if num.isdigit()]
    # numbers = map(int, numbers)
    # return sign * sum(numbers)

if __name__ == "__main__":
    data_folder = "drive_data/"
    files = os.listdir(data_folder)

    langs = ["en-GB", "en-GB", "en-GB", "ru-RU", "ru-RU", "ur-IN"]
    for f, lang in zip(files[:], langs[:]):
        audiofile = data_folder + f
        # print(audiofile)
        processSpeech(audiofile, "income", lang=lang)