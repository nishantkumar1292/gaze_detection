import subprocess
import os
from utils.pydub import AudioSegment, utils as pydub_utils
import array
# import matplotlib.pyplot as plt

#for clustering
import pandas as pd
from sklearn.cluster import KMeans
import multiprocessing
import numpy as np
# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import MinMaxScaler
# import seaborn as sns
# import matplotlib.pyplot as plt


video_file = "videos/219095af50dc70186620180511085807.mp4"

def convert_to_audio(video_file):
	directory = 'audios'
	if not os.path.exists(directory):
		os.makedirs(directory)
	audio_file_name = video_file.split("/")[1].split(".")[0] + ".wav"
	audio_path = os.path.join(directory, audio_file_name)
	if not os.path.exists(audio_path):
		command = "ffmpeg -i {} -vn {}".format(video_file, audio_path)
		subprocess.call(command, shell=True)
	return audio_path

def segmented_audio(audio_path):
	audio = AudioSegment.from_wav(audio_path)
	segement_length = 3*1000 #pydub does things in millseconds
	#filter out segments where there is long periods of silence or where noise is predominant. we use segment's pitch value for this purpose
	bit_depth = audio.sample_width * 8
	array_type = pydub_utils.get_array_type(bit_depth)
	numeric_array = array.array(array_type, audio._data)
	plt.plot(numeric_array)
	plt.ylabel('some numbers')
	plt.show()

def get_features(audio_file):
	from bregman.suite import Chromagram
	F = Chromagram(audio_file, nfft=16384, wfft=8192, nhop=2205)
	#F.X = all chroma features
	return F.X

def get_features_new(audio_file):
	from python_speech_features import mfcc
	import scipy.io.wavfile as wav
	(rate,sig) = wav.read(audio_file)
	mfcc_feat = mfcc(sig,rate)
	print("mfcc", mfcc_feat)
	return mfcc_feat


def clustering(features):
	data = pd.DataFrame(features.T)
	kmeans = KMeans(n_clusters=2, n_jobs=multiprocessing.cpu_count()-1, max_iter=600) # Number of clusters must be 3 - one for one speaker, one for other and one for noise
	kmeans.fit(data)
	labels = kmeans.predict(data)
	unique, counts = np.unique(labels, return_counts=True)
	return counts

def get_second_speaker_score(counts, features):
	score = abs((counts[0] - counts[1])/2.0)/(features.shape[1]*1.0)
	return score

def download_video(url):
	directory = 'videos'
	if not os.path.exists(directory):
		os.makedirs(directory)
	video = url.split("/")[-1]
	video_path = os.path.join(directory, video)
	if not os.path.exists(video_path):
		urllib.urlretrieve (url, video_path)
	return video_path

def get_multispeaker_score(url):
	video_file = download_video(url)
	#from video extract audio
	audio_path = convert_to_audio(video_file)
	features = get_features_new(audio_path)
	
	counts = clustering(features)
	score = get_second_speaker_score(counts, features)
	insight = False
	if score>0.5:
		insight = True
	return {"score": get_second_speaker_score(counts, features), "insight": insight}
