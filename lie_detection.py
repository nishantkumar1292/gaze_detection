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

def get_lie_score(video_path):
	response = get_lie_detection(video_path)
	return response