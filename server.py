from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

@app.route('/')
def check():
	return 'Server Running!!'

@app.route('/gaze_detect')
def get_gaze_detection():
	video = request.args.get('video')
	if video not in ["sample1", "sample2", "sample3"]:
		return jsonify({"error": "video not found"})
	elif video == "sample1":
		result = {"external_help_score": 38.6, "score_confidence": 92, "score_result": "cheating", "video": video, "directions":{"center": 60.5, "top": 30.2, "top_right":0, "right": 8.4, "right_bottom": 0, "bottom": 0, "bottom_left": 0.4, "left": 0.5, "left_top": 0} }
	elif video == "sample2":
		result = {"external_help_score": 21.2, "score_confidence": 93, "score_result": "not cheating", "video": video, "directions":{"center": 53.5, "top": 10.5, "top_right":0, "right": 10.8, "right_bottom": 1.7, "bottom": 1.5, "bottom_left": 1.4, "left": 10.7, "left_top": 0} }
	elif video == "sample3":
		result = {"external_help_score": 19.2, "score_confidence": 92, "score_result": "not cheating", "video": video, "directions":{"center": 70.4, "top": 12.6, "top_right": 6.6, "right": 3.5, "right_bottom": 0, "bottom": 0, "bottom_left": 0.3, "left": 6.2, "left_top": 0.5} }
	else:
		result = {"error": "some internal error"}
	return jsonify(result)

if __name__ == '__main__':
	app.run(host='0.0.0.0')