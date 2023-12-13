from django.contrib import admin
from .models import MidiFile

class MidiFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'file_hash')
admin.site.register(MidiFile, MidiFileAdmin)
# Register your models here.
