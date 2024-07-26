from flask import Flask, render_template, send_file
import os
from datetime import datetime
from detect import download_video, detect_objects
from utils import create_webcam_url

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    input_video = "input.mp4"
    output_video = "output.mp4"  # Ensure it saves to static directory
    specific_time = datetime.now()
    specific_time_str = specific_time.strftime('%Y%m%d%H%M%S')
    video_url = create_webcam_url(specific_time_str)
    download_video(video_url, input_video)
    detect_objects(input_video, output_video, num_frames=30)

    return send_file('input.mp4', mimetype='video/mp4')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
