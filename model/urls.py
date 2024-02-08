from django.urls import path
from . import views

urlpatterns = [
	path("speech-to-speech", views.translate_audio_view)
]
