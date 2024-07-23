# Function to  create webcam url
import os
import requests


def create_webcam_url(specific_time_str):
    # Base URL and static parameters
    base_url = 'https://www.holidayinfo.cz/hol3_data.php'
    params = {'type': 'camvideo', 'ext': 'mp4', 'camid': '2131', 'cdt': specific_time_str, 'dt': specific_time_str}
    # Add datetime parameter to the params dictionary
    # Construct the final URL
    stream_url = f"{base_url}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
    return stream_url


# Function to download the video stream
def download_stream(url, output_path):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f'Successfully downloaded the stream to {output_path}')
    except requests.exceptions.RequestException as e:
        print(f'Failed to download the stream: {e}')


# Function to download web stream localy
def download_webcam_stream_specific_time(specific_time_str, stream_downld_folder):
    stream_url = create_webcam_url(specific_time_str)
    stream_file_name = 'webcam_stream_{}.mp4'.format(specific_time_str)
    output_file = os.path.join(stream_downld_folder, stream_file_name)
    download_stream(stream_url, output_file)
