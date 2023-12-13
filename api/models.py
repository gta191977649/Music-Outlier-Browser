from django.db import models
import hashlib

class MidiFile(models.Model):
    file = models.FileField(upload_to='midis/')
    file_hash = models.CharField(max_length=64, unique=True, null=True)  # Length 64 for SHA256

