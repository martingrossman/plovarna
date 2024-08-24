# Function to  create webcam url
import os
import shutil
import requests
import cv2
import re


def create_webcam_url(specific_time_str):
    # Base URL and static parameters
    base_url = 'https://www.holidayinfo.cz/hol3_data.php'
    params = {'type': 'camvideo', 'ext': 'mp4', 'camid': '2131', 'cdt': specific_time_str, 'dt': specific_time_str}
    # Add datetime parameter to the params dictionary
    # Construct the final URL
    stream_url = f"{base_url}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
    return stream_url


def download_stream(url, output_path):
    # Function to download the video stream
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f'Successfully downloaded the stream to {output_path}')
    except requests.exceptions.RequestException as e:
        print(f'Failed to download the stream: {e}')


def download_webcam_stream_specific_time(specific_time_str, stream_downld_folder):
    # Function to download web stream localy
    stream_url = create_webcam_url(specific_time_str)
    stream_file_name = 'webcam_stream_{}.mp4'.format(specific_time_str)
    output_file = os.path.join(stream_downld_folder, stream_file_name)
    download_stream(stream_url, output_file)


def extract_frames(video_path):
    # Extracts png frames from video and places in the same directory
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    # Check if the video was opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
    else:
        # Initialize frame count
        frame_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # Read frames in a loop
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Could not read frame. Last frame = {}".format(frame_count))
                break
            frame_count += 1
            # Check if the current frame is the target frame
            if frame_count <= total_frames:
                # Save the frame as an image file
                video_folder_path = os.path.dirname(video_path)
                video_name = os.path.basename(video_path)
                video_name = video_name.split('.')[0]
                frame_name = f"{video_name}{'_' + str(frame_count).zfill(4)}{'.png'}"
                frame_path = os.path.join(video_folder_path, frame_name)

                cv2.imwrite(frame_path, frame)
            else:
                break

        # Release the video capture object
        cap.release()


def get_files_lst(directory, extension="mp4"):
    # returns path and names of files in directory by extension
    videos_path_lst = []
    videos_names_lst = []
    for file in os.listdir(directory):
        if file.endswith(extension):
            videos_path_lst.append(os.path.join(directory, file))
            videos_names_lst.append(file)
    return videos_path_lst, videos_names_lst


def get_time_from_filename(name, dirname=True, extension='png'):
    #  returns hour from  dir name and hour anf frame from image_name
    # Check if frame_name is a directory
    # try:
    #     frame_name = 'webcam_stream_20240701190000_125'  # This could be a directory name
    #     hour, last_digits = get_time_from_filename(frame_name)
    #     print(hour)  # Outputs: 19
    #     print(last_digits)  # Outputs: 125
    # except ValueError as e:
    #     print(e)
    #

    if dirname:
        pattern = rf'_(\d{{8}})(\d{{2}})\d{{4}}$'
    else:
        pattern = rf'_(\d{{8}})(\d{{2}})\d{{4}}_(\d+)\.{extension}$'

    match = re.search(pattern, name)

    if match:
        if dirname:
            hour = int(match.group(2))
            number = -1
            return hour, number
        else:
            hour = int(match.group(2))
            number = int(match.group(3))
            return hour, number

    else:
        # Raise an error if the filename does not match the expected pattern
        raise ValueError("Filename format is incorrect")


def sort_imgs_to_sep_dirs(src_video_dir, video_dest_folder):
    # sorts videos into separate directories based on name
    # src_video_dir = r'f:\plovarna\stream_videos_orig'
    # video_dest_folder = r'f:\plovarna\stream_videos_orig\videos'
    video_path_src_lst, _ = get_files_lst(src_video_dir, 'mp4')
    images_path_lst, images_names_lst = get_files_lst(src_video_dir, 'png')

    for video_path in video_path_src_lst:
        filename = os.path.basename(video_path)
        filename_woext = filename.split('.')[0]
        dest_folder = os.path.join(video_dest_folder, filename_woext)
        os.makedirs(dest_folder, exist_ok=True)
        dest_video_name = os.path.join(dest_folder, filename)
        shutil.move(video_path, dest_video_name)

        for img_p, im_n in zip(images_path_lst, images_names_lst):
            if filename_woext in im_n:
                dst_img = os.path.join(dest_folder, im_n)
                shutil.move(img_p, dst_img)