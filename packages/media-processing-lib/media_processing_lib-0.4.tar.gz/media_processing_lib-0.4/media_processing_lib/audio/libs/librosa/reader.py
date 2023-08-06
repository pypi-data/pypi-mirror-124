import librosa

def readAudio(path, **kwargs):
	if "sampleRate" in kwargs:
		kwargs["sr"] = kwargs["sampleRate"]
		del kwargs["sampleRate"]

	return librosa.load(path, **kwargs)
