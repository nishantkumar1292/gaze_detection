import cv2
import math
import numpy as np
import pandas as pd
import urllib
import os
import requests
import threading
import redis

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyes_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def analyse_video(video_path, frame_rate):
	distances, angles, video_frames, face_frames, eye_frames = get_gaze_points(video_path, frame_rate)
	external_help_score = get_gaze_analysis(distances, angles)
	face_confidence, eye_confidence = (face_frames*1.0)/video_frames, (eye_frames*1.0)/video_frames
	insight = False
	if external_help_score>70:
		insight = True
	response = {"face_confidence": face_confidence, "eye_confidence": eye_confidence, "gaze_score": external_help_score, "insight": insight}
	return response


def get_gaze_points(video_path, frame_rate):
	distances = []
	angles = []
	cap = cv2.VideoCapture(video_path)
	video_frames = 0
	counted_frames = 0
	face_frames = 0
	eye_frames = 0
	while cap.isOpened():
		ret, img = cap.read()
		if img is None:
			cap.release()
			break
		video_frames += 1		
		if (video_frames-1)%frame_rate != 0:
			continue
		counted_frames += 1
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray)
		for (x,y,w,h) in faces:
			face_frames += 1
			face_gray = gray[y:y+h, x:x+w]
			eyes = eyes_cascade.detectMultiScale(face_gray)
			for (ex,ey,ew,eh) in eyes:
				eye_frames += 0.5
				eye_center = (ex+ew/2,ey+eh/2)
				eyes_gray = face_gray[ey:ey+eh, ex:ex+ew]
				(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(eyes_gray) #minLoc is the location for minimumm intensity
				# print("eye_center", (ew/2, eh/2))
				# print("eye_ball", minLoc)

				#calculating distance and angle
				distance = math.sqrt(math.pow(ew/2-minLoc[0],2) + math.pow(eh/2-minLoc[1],2))
				angle = math.degrees(math.atan2(minLoc[1]-eh/2, minLoc[0]-ew/2))
				distances.append(distance)
				angles.append(angle)
				if len(distances)%10==0:
					print("{} frames done".format(len(distances)))
	return distances, angles, counted_frames, face_frames, eye_frames

def get_gaze_analysis(distances, angles):
	#constriants
	threshold_distance = 10

	#analysis
	np_distances = np.array(distances)
	np_angles = np.array(angles)
	df = pd.DataFrame({'distance': np_distances, 'angle': np_angles})
	score = get_score(df, threshold_distance)
	return score

def get_score(df, threshold_distance):
	total_row_count = df.shape[0]
	if total_row_count == 0:
		total_row_count = 1.0
	filtered_row_count = df[df['distance']>threshold_distance].shape[0]
	if (filtered_row_count*1.0)/total_row_count<0.3:
		return 0.0
	else:
		df['label'] = df.apply(get_label, axis=1)
		grouped_count = df[df['distance']>threshold_distance].groupby(['label']).size().reset_index(name='counts').sort_values(by=['counts']).shape[0]
		return (((8-grouped_count)*1.0)/8)*100



def get_label(row):
	if 0<=row['angle']<45 or -360<=row['angle']<-315:
		return '0-45'
	elif 45<=row['angle']<90 or -315<=row['angle']<-270:
		return '45-90'
	elif 90<=row['angle']<135 or -270<=row['angle']<-225:
		return '90-135'
	elif 135<=row['angle']<180 or -225<=row['angle']<-180:
		return '135-180'
	elif 180<=row['angle']<225 or -180<=row['angle']<-135:
		return '180-225'
	elif 225<=row['angle']<270 or -135<=row['angle']<-90:
		return '225-270'
	elif 270<=row['angle']<315 or -90<=row['angle']<-45:
		return '270-315'
	elif 315<=row['angle']<360 or -45<=row['angle']<0:
		return '315-360'
	else:
		return "NA"

# run_for_video('https://s3.ap-south-1.amazonaws.com/fjinterviewanswersmumbai/209115a3d1a1b81f3620171222201339.mp4')
# analyse_video(0)