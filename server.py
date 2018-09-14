from flask import Flask
from flask import jsonify
from flask import request

#file imports
from gaze_detection import run_for_video

app = Flask(__name__)

@app.route('/')
def check():
	return 'Server Running!!'

@app.route('/gaze_detect')
def get_gaze_detection():
	video_url = request.args.get('url')
	result =  run_for_video(url)
	return jsonify(result)

if __name__ == '__main__':
	app.run(host='0.0.0.0')