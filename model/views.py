from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .seamless import translate_audio  # Import your translation function

@api_view(['POST'])
def translate_audio_view(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio')
        if audio_file:
            # Process the audio file
            translated_audio = translate_audio(audio_file)
            # Return the translated audio file
            return JsonResponse({'translated_audio': translated_audio})
        else:
            return JsonResponse({'error': 'No audio file provided'}, status=400)
    else:
        return "Hello world"