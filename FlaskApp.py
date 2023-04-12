from flask import Flask, render_template
import AudioCapture
import Wav2Text

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/Capture", methods=['POST'])
def capture():
    AudioCapture.CaptureAudio()
    converted_text=Wav2Text.conv_wav2text()
    
    return render_template("result.html",textboxdata=)

if __name__ == "__main__":
    app.run(debug=True)