import torchaudio
import torch
from transformers import AutoProcessor, SeamlessM4TModel
processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-large")
model = SeamlessM4TModel.from_pretrained("facebook/hf-seamless-m4t-large")

def translate_audio(audio_file):
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-large")
	model = SeamlessM4TModel.from_pretrained("facebook/hf-seamless-m4t-large")
	model = model.to(device)
	audio, orig_freq =  torchaudio.load(audio_file)
	audio =  torchaudio.functional.resample(audio, orig_freq=orig_freq, new_freq=16_000) # must be a 16 kHz waveform array
	audio_inputs = processor(audios=audio, return_tensors="pt")
	audio_inputs = audio_inputs.to(device)
	audio_array_from_audio = model.generate(**audio_inputs, tgt_lang="rus")[0].cpu().numpy().squeeze()
	return audio_array_from_audio