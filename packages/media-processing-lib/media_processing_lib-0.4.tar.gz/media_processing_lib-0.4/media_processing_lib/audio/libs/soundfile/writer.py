import soundfile
from ...mpl_audio import MPLAudio
from ....debug import Debug

def writeAudio(audio:MPLAudio, path:str, **kwargs):
    Debug.log(1, "[soundfile::writeAudio] Writing %s to %s." % (str(audio), path))
    soundfile.write(path, audio.data, int(audio.sampleRate))
