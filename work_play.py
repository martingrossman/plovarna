from datetime import datetime
from utils import create_webcam_url

specific_time = datetime(2024, 7, 26, 10, 0)
specific_time_str = specific_time.strftime('%Y%m%d%H%M%S')
print(create_webcam_url(specific_time_str))


specific_time = datetime.now()
specific_time_str = specific_time.strftime('%Y%m%d%H%M%S')
print(create_webcam_url(specific_time_str))