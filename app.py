from flask import Flask, render_template, send_file
import os
import threading
import time
from datetime import datetime
from detect import download_video, detect_objects
from utils import create_webcam_url

app = Flask(__name__)
video_saved = False  # Global flag to indicate if the video has been processed and saved
final_output_video = "output.mp4"  # Path where the final video will be saved
processing_lock = threading.Lock()  # Lock to prevent concurrent processing

NUM_FRAMES = 30
CONFIDENCE = 0.25
VERBOSE = True
UPDATE_WAIT_S = 1800



def process_video():
    global video_saved, final_output_video

    # Acquire the lock before starting the video processing
    with processing_lock:
        input_video = "input.mp4"
        temp_output_video = "temp_output.mp4"

        specific_time = datetime.now()
        specific_time_str = specific_time.strftime('%Y%m%d%H%M%S')
        video_url = create_webcam_url(specific_time_str)
        download_video(video_url, input_video)

        detect_objects(input_video, temp_output_video, final_output_video, num_frames=NUM_FRAMES,
                       confidence_threshold=CONFIDENCE, verb=VERBOSE)

        # Set the flag to True after processing and saving the video
        video_saved = True

def scheduled_video_update():
    while True:
        # Only process the video if the lock is not held (i.e., no processing is currently happening)
        if not processing_lock.locked():
            print('run process scheduled')
            process_video()
        time.sleep(UPDATE_WAIT_S)  # Wait for 1 hour (3600 seconds) before attempting the next video download

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    # Return the already processed video
    return send_file(final_output_video, mimetype='video/mp4')

if __name__ == "__main__":
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=scheduled_video_update)
    scheduler_thread.daemon = True  # Ensure that the thread will exit when the main program exits
    scheduler_thread.start()

    # Start the Flask app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
