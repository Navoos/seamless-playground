from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.http import JsonResponse, HttpResponse, FileResponse
from rest_framework.decorators import api_view
from .seamless import translate_audio  # Import your translation function
from .forms import UploadFileForm
import os

@api_view(['POST'])
@csrf_exempt
def translate_audio_view(request):
		if request.method == 'POST':
				form = UploadFileForm(request.POST, request.FILES)
				if form.is_valid():
						# Process the audio file
						lang = request.data['target']
						print(request.data['target'])
						translated_audio = translate_audio(request.FILES['file'], request.POST.get("target", None))
						file_path = "/Users/yakhoudr/goinfre/seamless-playground/translated_audio.wav"
						f = open(file_path, "rb") 
						response = HttpResponse()
						response.write(f.read())
						response['Content-Type'] = 'audio/wav'
						response['Content-Length'] =os.path.getsize(file_path)
						return response
				else:
						return JsonResponse({'error': 'No audio file provided'}, status=400)
		else:
				return "Hello world"
