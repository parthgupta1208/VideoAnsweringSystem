import cv2
import pyaudio
import wave
import numpy as np
import moviepy.editor as mp
import threading

# Define constants for recording settings
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "audio.wav"
VIDEO_OUTPUT_FILENAME = "output.mp4"

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

    # Save the wav file 
    wavfile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wavfile.setnchannels(1)
    wavfile.setsampwidth(2)
    wavfile.setframerate(RATE)
    wavfile.writeframes(b''.join(audio_frames))
    wavfile.close()

# Start audio recording and video showing threads
audio_thread = threading.Thread(target=record_audio)
video_thread = threading.Thread(target=show_video)
audio_thread.start()
video_thread.start()