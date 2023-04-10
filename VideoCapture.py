import cv2
import pyaudio
import wave
import numpy as np
import moviepy.editor as mp

# Define constants for recording settings
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "audio.wav"
VIDEO_OUTPUT_FILENAME = "output.mp4"

# Initialize audio recording
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Initialize video recording
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(VIDEO_OUTPUT_FILENAME, fourcc, 20.0, (640,480))

# Record audio and video until spacebar is pressed
frames = []
while True:
    # Check if spacebar has been pressed
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

    # Record audio
    data = stream.read(CHUNK)
    frames.append(np.frombuffer(data, dtype=np.int16))

    # Record video
    ret, frame = cap.read()
    if ret:
        out.write(frame)
        cv2.imshow('Press Spacebar to Stop Recording', frame)


# Stop recording
stream.stop_stream()
stream.close()
audio.terminate()
cap.release()
out.release()

# Save audio as WAV file
wavfile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wavfile.setnchannels(1)
wavfile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
wavfile.setframerate(RATE)
wavfile.writeframes(b''.join(frames))
wavfile.close()

# Combine audio and video into a single MP4 file
audio_clip = mp.AudioFileClip(WAVE_OUTPUT_FILENAME)
video_clip = mp.VideoFileClip(VIDEO_OUTPUT_FILENAME)
final_clip = video_clip.set_audio(audio_clip)
final_clip.write_videofile("final_output.mp4")
