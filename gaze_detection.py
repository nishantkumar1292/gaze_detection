import cv2
import math

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyes_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def get_video(video_url):
	video_path = download_video(video_url)
	return video_path

def analyse_video(video_path):
	distances, angles = get_gaze_points(video_path)
	gaze_analysis = get_gaze_analysis(distances, angles)


def get_gaze_points(video_path):
	distances = []
	angles = []
	cap = cv2.VideoCapture(video_path)
	while cap.isOpened():
		ret, img = cap.read()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray)
		for (x,y,w,h) in faces:
			face_gray = gray[y:y+h, x:x+w]
			eyes = eyes_cascade.detectMultiScale(face_gray)
			for (ex,ey,ew,eh) in eyes:
				eye_center = (ex+ew/2,ey+eh/2)
				eyes_gray = face_gray[ey:ey+eh, ex:ex+ew]
				(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(eyes_gray) #minLoc is the location for minimumm intensity
				print("eye_center", (ew/2, eh/2))
				print("eye_ball", minLoc)

				#calculating distance and angle
				distance = math.sqrt(math.pow(ew/2-minLoc[0],2) + math.pow(eh/2-minLoc[1],2))
				angle = math.degrees(math.atan2(minLoc[1]-eh/2, minLoc[0]-ew/2))
				distances.append(distance)
				angles.append(angle)
	return distances, angles

def get_gaze_analysis():
	pass

analyse_video(0)