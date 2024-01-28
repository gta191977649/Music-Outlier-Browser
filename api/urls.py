from django.urls import path
from api import views
from .views import MidiFileUploadView,AudioFileUploadView

urlpatterns = [
    path('search/', views.search, name='api'),
    path('cluster/', views.cluster, name='api'),
    path('midi-upload/', MidiFileUploadView.as_view(), name='midi-file-upload'),
    path('audio-upload/', AudioFileUploadView.as_view(), name='audio-file-upload'),
]