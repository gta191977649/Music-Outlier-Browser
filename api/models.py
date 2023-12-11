from django.db import models

class MidiFile(models.Model):
    file = models.FileField(upload_to='midis/')
