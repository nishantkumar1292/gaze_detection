from flask import Flask
from flask import jsonify
from flask import request

#file imports
from gaze_detection import run_for_video
from speaker_detection import get_multispeaker_score
from lie_detection import get_lie_score
app = Flask(__name__)

@app.route('/')
def check():
	return 'Server Running!!'

@app.route('/gaze_detect')
def get_gaze_detection():
	video_url = request.args.get('url')
	if video_url:
		gaze_result =  run_for_video(video_url)
		spekaer_result = get_multispeaker_score(video_url)
		lie_score = get_lie_score(video_url)
		result = {"gaze_result": gaze_result, "spekaer_result": spekaer_result, "lie_score": lie_score}
	else:
		result = {"error": "url not found"}
	return jsonify(result)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)