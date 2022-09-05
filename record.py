import pyaudio, wave, playsound, numpy
import speech_recognition as sr
from scipy.io.wavfile import read, write
from difflib import SequenceMatcher

def record(time):
	r = sr.Recognizer()
	mic = sr.Microphone()
	with mic as source:
		r.adjust_for_ambient_noise(source)
		audio = r.record(source, duration=time)
	print("Translate original:", r.recognize_google(audio, language='ru-RU').lower().encode("cp866").decode("cp1251"))
	return audio.frame_data

def save(data, sample_format, channels, fps, filename):
	p = pyaudio.PyAudio()
	wf = wave.open(filename, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(p.get_sample_size(sample_format))
	wf.setframerate(fps)
	wf.writeframes(data)
	wf.close()

def getbeepfragment(fps, stream):
	data = stream
	data_len = len(data)
	buffer = 1*fps
	max_val1 = 0
	max_val2 = 0
	peak1 = 0
	peak2 = 0
	idx = 0
	while idx < len(data):
		if data[idx] > max_val1:
			max_val1 = data[idx]
			peak1 = idx
		idx += 1
	idx = 0
	while idx < len(data):
		if data[idx] > max_val2 and data[idx] < max_val1 and not (idx > peak1-buffer and idx < peak1+buffer):
			max_val2 = data[idx]
			peak2 = idx
		idx += 1
	# print("data len:", data_len, "peak inx1:", peak1, "max volume1:", max_val1, "peak inx2:", peak2, "max volume2:", max_val2)
	if peak1 < peak2:
		export = data[peak1:peak2]
	else:
		export = data[peak2:peak1]
	return export  

def speech2text(stream):
	r = sr.Recognizer()
	harvard = sr.AudioFile(stream)
	with harvard as source:
		r.adjust_for_ambient_noise(source)
		audio = r.record(source)
	return r.recognize_google(audio, language='ru-RU', show_all=False).lower().encode("cp866").decode("cp1251")

def gettext():
	numpy.set_printoptions(threshold=numpy.inf)
	r = sr.Recognizer()
	
	print("Recording start")
	data = record(20)
	print("Recording stop")
	get = getbeepfragment(44100, numpy.frombuffer(data, dtype=numpy.int16))
	# save(get, pyaudio.paInt16, 1, 44100, "output.wav")
	
	audio_source = sr.AudioData(bytes(get), 44100, 2)
	return r.recognize_google(audio_source, language='ru-RU', show_all=False).lower().encode("cp866").decode("cp1251")

if __name__ == '__main__':
	input("PAUSE")
	str1 = gettext()
	# str1 = speech2text("track1.wav")
	print("Translate cut:", str1)
	input("PAUSE")
	str2 = gettext()
	# str2 = speech2text("track2.wav")
	print("Translate cut:", str2)
	input("PAUSE")
	s = SequenceMatcher(None, str1, str2)
	print(s.ratio() * 100, "%")
	
	