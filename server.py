from flask import Flask
from flask import jsonify
from flask import request

#file imports
from gaze_detection import run_for_video
from speaker_detection import get_multispeaker_score
from lie_detection import get_lie_score
from utils import helper

app = Flask(__name__)

@app.route('/')
def check():
	return 'Server Running!!'

@app.route('/gaze_detect')
def get_gaze_detection():
	video_url, frame_rate = helper.get_request_params(request)
	if video_url:
		response = helper.download_video(video_url)
		if response["success"]:
			video_path = response["video_path"]
			gaze_result =  analyse_video(video_path, frame_rate)
			speaker_result = get_multispeaker_score(video_path, frame_rate)
			lie_score = get_lie_score(video_path)
			result = {"gaze_result": gaze_result, "speaker_result": speaker_result, "lie_score": lie_score}
		else:
			result = {"error": response["error"]}
	else:
		result = {"error": "url not found"}
	return jsonify(result)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)