from flask import Flask, render_template
import AudioCapture

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/Capture", methods=['POST'])
def capture():
    AudioCapture.CaptureAudio()
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)