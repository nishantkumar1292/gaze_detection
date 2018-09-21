import os
import subprocess
import json

def get_lie_detection(video_path):
	current_path = os.path.dirname(os.path.abspath(__file__))
	abs_video_path = os.path.join(current_path, video_path)
	command = "/home/ubuntu/vdohireai/bin/lie_detection.sh {}".format(abs_video_path)
	print(command)
	subprocess.call(command, shell=True)
	output_path = "/home/ubuntu/vdohireai/response.txt"
	response = {}
	with open(output_path, 'r') as file:
		response = json.load(file)
	return response

def download_video(url):
	directory = 'videos'
	if not os.path.exists(directory):
		os.makedirs(directory)
	video = url.split("/")[-1]
	video_path = os.path.join(directory, video)
	if not os.path.exists(video_path):
		urllib.urlretrieve (url, video_path)
	return video_path

def get_lie_score(url):
	video_path = download_video(url)
	response = get_lie_detection(video_path)
	return response