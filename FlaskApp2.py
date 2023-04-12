import cv2
import pyaudio
import wave
import numpy as np
import moviepy.editor as mp
import threading
from flask import Flask, render_template
import openai
import os
import speech_recognition as sr
import markdown2

# setup flask
app = Flask(__name__)
awaiter=0

# home route
@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/Capture", methods=['POST'])
def CaptureAudio():
    # Creating awaiter variable so that program waits for module to complete execution before progressing
    global awaiter
    awaiter=1
    
    # Define constants for recording settings
    RATE = 44100
    CHUNK = 1024
    WAVE_OUTPUT_FILENAME = "audio.wav"

    # Initialize audio recording
    audio_frames = []
    audio_event = threading.Event()

    def record_audio():
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

        while not audio_event.is_set():
            data = stream.read(CHUNK)
            audio_frames.append(np.frombuffer(data, dtype=np.int16))

        stream.stop_stream()
        stream.close()
        audio.terminate()

    # Initialize video recording
    video_frames = []
    video_event = threading.Event()

    def show_video():
        global awaiter
        cap = cv2.VideoCapture(0)

        while not video_event.is_set():
            ret, frame = cap.read()
            if ret:
                video_frames.append(frame)
                cv2.imshow('Press Spacebar to Stop Recording', frame)
                if cv2.waitKey(1) & 0xFF == ord(' '):
                    break

        cap.release()
        cv2.destroyAllWindows()

        # Stop recording and save audio and video files
        video_event.set()
        audio_event.set()
        audio_thread.join()

        # Save the wav file  & update awaiter
        wavfile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wavfile.setnchannels(1)
        wavfile.setsampwidth(2)
        wavfile.setframerate(RATE)
        wavfile.writeframes(b''.join(audio_frames))
        wavfile.close()
        awaiter=0

    # Start audio recording and video showing threads
    audio_thread = threading.Thread(target=record_audio)
    video_thread = threading.Thread(target=show_video)
    audio_thread.start()
    video_thread.start()

    # check if program has terminated
    while awaiter!=0:
        pass
    
    # convert wav to text and feed to gpt
    r = sr.Recognizer()
    with sr.AudioFile('audio.wav') as source:
        audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    openai.api_key = os.getenv("OPENAI_KEY")
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages = [{"role": "system", "content" : "You are FridayAI, a large language model trained by Parth Gupta. Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-04-10"},
    {"role": "user", "content" : "How are you?"},
    {"role": "assistant", "content" : "I am doing well"},
    {"role": "user", "content" : text}]
    )
    print(completion['choices'][0]['message']['content'])
    html = markdown2.markdown(completion['choices'][0]['message']['content'])
    return render_template("result.html", textboxdata=html)


# @app.route("/GetOutput", methods=['POST'])

if __name__ == "__main__":
    app.run(debug=True)