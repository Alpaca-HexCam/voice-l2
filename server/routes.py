# coding=utf-8

from server import app
from flask import request, jsonify, redirect, url_for
import speech_recognition as sr
import os
import words2num
import re
from googletrans import Translator
from pydub import AudioSegment
import json
import requests

import firebase_admin
from firebase_admin import credentials, db, firestore, storage

firebase_admin.initialize_app()
db = firestore.client()
storage = storage.bucket("alpaca-72130.appspot.com")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        req = request.get_json()
        user_id = req["user_id"]
        path = req["path"]
        blob = storage.blob(path)
        blob.download_to_filename("/tmp/test.ogg")

        audio = AudioSegment.from_ogg("/tmp/test.ogg")
        audio.export("/tmp/test.wav", format="wav")

        value, type = processSpeech("/tmp/test.wav")
        if value is not None:
            data = {
                "command_type": type,
                "amount": value,
                "user_id": user_id
            }
            return jsonify(data)
    else:
        return "ERROR"
    return "OK"

@app.route('/test', methods=['GET', 'POST'])
def test():
    return "Received"

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


def processSpeech(audio_file, lang="en-GB"):
    # Type is one of ["add", "subtract", "general"]

    text = speechToText(audio_file, lang)
    if text is None:
        return None

    if not lang == "en-GB":
        translator = Translator()
        text = translator.translate(text, src=lang[:2], dest="en").text

    if text is None:
        return None

    words = text.split()

    income = ["made", "earned", "salary", "earn"]
    expense = ["bought", "spent", "shop"]

    if len(list(set(words) & set(income))) > 0:
        type = "add"
    elif len(list(set(words) & set(expense))) > 0:
        type = "subtract"
    else:
        type = "general"
    print(text)
    val = 0
    for w in words:
        w = re.sub('[$£,]', '', w)
        try:
            if w.isdigit():
                val += float(w)
            else:
                val += words2num.words2num(w)
        except:
            pass

    return val, type