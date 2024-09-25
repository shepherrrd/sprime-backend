import requests
import json

url = 'http://127.0.0.1:8000/upload_video'

# Corrected file path
video_file_path = r'C:\Users\goldo\Downloads\Untitled video - Made with Clipchamp.mp4'

files = {'video_file': open(video_file_path, 'rb')}

# Define the scenes list
scenes = [
    {'start_time': 0.0, 'end_time': 30.0}
]

# Convert scenes list to JSON string
data = {'scenes': json.dumps(scenes)}

response = requests.post(url, files=files, data=data)
print(response.json())
