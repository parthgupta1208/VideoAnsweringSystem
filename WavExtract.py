from moviepy.editor import *
def startExtract(filename):
    video = VideoFileClip(filename)
    audio = video.audio
    audio.write_audiofile("audio.wav")