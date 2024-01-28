from rest_framework import serializers
from .models import MidiFile,AudioFile

class MidiFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MidiFile
        fields = ['file']
class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ['file']


