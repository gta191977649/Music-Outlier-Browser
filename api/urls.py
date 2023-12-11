from django.urls import path
from api import views
from .views import MidiFileUploadView

urlpatterns = [
    path('search/', views.search, name='api'),
    path('cluster/', views.cluster, name='api'),
    path('midi-upload/', MidiFileUploadView.as_view(), name='midi-file-upload'),
]