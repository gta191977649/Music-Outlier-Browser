from rest_framework import serializers
from .models import MidiFile

class MidiFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MidiFile
        fields = ['file']
