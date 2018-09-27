import requests
import urllib

def is_url_valid(url):
	try:
		r = requests.head(url)
	except requests.exceptions.MissingSchema as err:
		return False, str(err)
	return r.status_code == requests.codes.ok, "file not found at url"

def download_video(url):
	truth_value, message = is_url_valid(video_url)
	if truth_value:
		directory = 'videos'
		if not os.path.exists(directory):
			os.makedirs(directory)
		video = url.split("/")[-1]
		video_path = os.path.join(directory, video)
		if not os.path.exists(video_path):
			urllib.urlretrieve (url, video_path)
		response = {"video_path": video_path, "success": True}
	else:
		response = {"success": False, "error": message}
	return response

def get_request_params(request):	
	video_url = request.args.get('url')
	"""frame_rate defines the frequency to pick up frames. For example if the frame_rate=1, every frame is picked up for processing. If the frame_rate=3, every 3rd frame is picked up and frame_rate=10 results in processing of every 10th frame."""
	frame_rate = request.args.get('frame_rate')
	try:
		frame_rate = int(frame_rate)
	except:
		frame_rate = 1
	return video_url, frame_rate