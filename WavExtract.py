from moviepy.editor import *

# Load the video file
video = VideoFileClip("video.mp4")

# Extract the audio from the video
audio = video.audio

# Save the audio as a .wav file
audio.write_audiofile("audio.wav")