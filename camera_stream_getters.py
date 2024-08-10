import requests
from bs4 import BeautifulSoup
import re


class WebcamDownloader:
    def __init__(self, base_url, camid):
        self.base_url = base_url
        self.camid = camid

    def get_latest_date(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')
            latest_time = None

            pattern = re.compile(rf'"{self.camid}".*?"lastdt":"(\d{{14}})"')

            for script in scripts:
                match = pattern.search(script.text)
                if match:
                    latest_time = match.group(1)
                    break

            if latest_time:
                return latest_time
            else:
                raise ValueError(f"Unable to find the latest recorded time for camera {camid}.")
        else:
            raise ConnectionError(f"Failed to fetch the webpage. Status code: {response.status_code}")

    def get_webcam_url(self, timestamp, ext='mp4'):
        # Base URL and static parameters
        video_url = f"{self.base_url}?type=camvideo&ext={ext}&camid={camid}&cdt={timestamp}"
        return video_url

    def create_webcam_url(self,timestamp):
        # Base URL and static parameters
        base_url = 'https://www.holidayinfo.cz/hol3_data.php'
        params = {'type': 'camvideo', 'ext': 'mp4', 'camid': self.camid, 'cdt': timestamp, 'dt': timestamp}
        # Add datetime parameter to the params dictionary
        # Construct the final URL
        stream_url = f"{base_url}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
        return stream_url

    @staticmethod
    def download_stream(self, video_url, ext='mp4'):
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            filename = f"webcam_{camid}.{ext}"
            with open(filename, 'wb') as video_file:
                for chunk in response.iter_content(chunk_size=8192):
                    video_file.write(chunk)
            print(f"Saved latest video to {filename}")
        else:
            raise ConnectionError(f"Failed to fetch the video stream. Status code: {response.status_code}")


# Example usage
base_url = "https://www.holidayinfo.cz/en-US/camera/2131"
base_url = 'https://www.holidayinfo.cz/cs/locinfo/podoli'
base_url = 'https://leto.holidayinfo.cz/cs/camera/benecko'
camid = "3126"
webcam_downloader = WebcamDownloader(base_url, camid)


latest_timestamp = webcam_downloader.get_latest_date()
print(f"Latest timestamp for camera {camid}: {latest_timestamp}")
strm_url = webcam_downloader.create_webcam_url(latest_timestamp)
webcam_downloader.download_stream(latest_timestamp, strm_url)

