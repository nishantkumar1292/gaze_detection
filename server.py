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
	result = {"external_help_confidence": 30, "video": video, "directions":{"center": 70, "top": 10, "top_right":1, "right": 0, "right_bottom": 0, "bottom": 0, "bottom_left": 5, "left": 10, "left_top": 4} }
	return jsonify(result)

if __name__ == '__main__':
	app.run()