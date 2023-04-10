import speech_recognition as sr
def conv_wav2text():
    r = sr.Recognizer()
    with sr.AudioFile('audio.wav') as source:
        audio_data = r.record(source)
    
    text = r.recognize_google(audio_data)
    return text