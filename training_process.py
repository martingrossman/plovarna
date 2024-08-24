import glob
import os
import shutil
from datetime import datetime
from utils import download_webcam_stream_specific_time
from utils import extract_frames
from utils import get_files_lst

# Download video for data collection each hour in TIME_RNG
MONTH = 8
DAY = 24
TIME_RNG = (8, 16)
VIDEOSTREAM_DOWNLOAD_FOLDER = r'f:\plovarna\stream_videos_orig\videos2'

for hr in range(*TIME_RNG):
    print(f'Downloading video hour {hr} of {TIME_RNG[1] - TIME_RNG[0]}')
    specific_time = datetime(2024, MONTH, DAY, hr, 0)
    specific_time_str = specific_time.strftime('%Y%m%d%H%M%S')
    download_webcam_stream_specific_time(specific_time_str, VIDEOSTREAM_DOWNLOAD_FOLDER)


# Extract images from videos in separate folders
videos_path_lst, videos_names_lst = get_files_lst(VIDEOSTREAM_DOWNLOAD_FOLDER)
for video_path, video_name in zip(videos_path_lst, videos_names_lst):
    # create separate video dir and copy to it video
    video_name_woext = video_name.split('.')[0]
    video_folder_dest = os.path.join(VIDEOSTREAM_DOWNLOAD_FOLDER, video_name_woext)
    video_path_dest = os.path.join(video_folder_dest, video_name)
    os.makedirs(video_folder_dest, exist_ok=True)
    shutil.copyfile(video_path, video_path_dest)
    print(video_path_dest)
    # extract the frames
    extract_frames(video_path_dest)








# get hour from name
video_name = videos_names_lst[0]

# sort imgaes into separate dir
import os
import shutil



