import torchaudio
from pydub import AudioSegment
import torch
import wave as wv
from scipy.io.wavfile import write
import numpy as np
from transformers import AutoProcessor, SeamlessM4TModel
import os
processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-large")
model = SeamlessM4TModel.from_pretrained("facebook/hf-seamless-m4t-large")

def translate_audio(audio_file_fd, target):
	with open("/Users/yakhoudr/goinfre/seamless-playground/" + audio_file_fd.name, "wb+") as destination:
		for chunk in audio_file_fd.chunks():
			destination.write(chunk)
	convert_to_wav("/Users/yakhoudr/goinfre/seamless-playground/" + audio_file_fd.name, "/Users/yakhoudr/goinfre/seamless-playground/" + "wav_format.wav")
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-large")
	model = SeamlessM4TModel.from_pretrained("facebook/hf-seamless-m4t-large")
	model = model.to(device)
	audio, orig_freq =  torchaudio.load("/Users/yakhoudr/goinfre/seamless-playground/" + "wav_format.wav")
	audio =  torchaudio.functional.resample(audio, orig_freq=orig_freq, new_freq=16_000) # must be a 16 kHz waveform array
	audio_inputs = processor(audios=audio, return_tensors="pt")
	audio_inputs = audio_inputs.to(device)
	audio_array_from_audio = model.generate(**audio_inputs, tgt_lang=target)[0].cpu().numpy().squeeze()
	audio_tensor = torch.from_numpy(audio_array_from_audio).float()
	if audio_tensor.ndim == 1:
		audio_tensor = audio_tensor.unsqueeze(0)  # Ensure it has a channel dimension
	sample_rate = 16000  # Define the sample rate
	torchaudio.save("translated_audio.wav", audio_tensor, sample_rate)
	return 'success'


def convert_to_wav(source_path, target_path):
    audio = AudioSegment.from_file(source_path)
    audio.export(target_path, format="wav")
