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

def record_video():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(VIDEO_OUTPUT_FILENAME, fourcc, 20.0, (640,480))

    while not video_event.is_set():
        ret, frame = cap.read()
        if ret:
            video_frames.append(frame)
            out.write(frame)
            cv2.imshow('Press Spacebar to Stop Recording', frame)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Stop recording and save audio and video files
    video_event.set()
    audio_event.set()
    audio_thread.join()

    wavfile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wavfile.setnchannels(1)
    wavfile.setsampwidth(2)
    wavfile.setframerate(RATE)
    wavfile.writeframes(b''.join(audio_frames))
    wavfile.close()

    audio_clip = mp.AudioFileClip(WAVE_OUTPUT_FILENAME)
    video_clip = mp.concatenate_videoclips([mp.VideoFileClip(VIDEO_OUTPUT_FILENAME)])
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile("final_output.mp4")

# Start audio and video recording threads
audio_thread = threading.Thread(target=record_audio)
video_thread = threading.Thread(target=record_video)
audio_thread.start()
video_thread.start()