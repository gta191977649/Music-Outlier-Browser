# Generated by Django 3.2.16 on 2023-12-13 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='midifile',
            name='file_hash',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
    ]
