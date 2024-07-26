from flask import Flask, render_template, send_file
import os
from datetime import datetime
from detect import download_video, detect_objects
from utils import create_webcam_url

app = Flask(__name__)
video_saved = False  # Global flag to indicate if the video has been processed and saved
final_output_video = "output.mp4"  # Path where the final video will be saved

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    global video_saved

    if not video_saved:
        input_video = "input.mp4"
        temp_output_video = "temp_output.mp4"

        specific_time = datetime.now()
        specific_time_str = specific_time.strftime('%Y%m%d%H%M%S')
        video_url = create_webcam_url(specific_time_str)
        download_video(video_url, input_video)

        detect_objects(input_video, temp_output_video, final_output_video, num_frames=10)

        # Set the flag to True after processing and saving the video
        video_saved = True

    return send_file(final_output_video, mimetype='video/mp4')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
