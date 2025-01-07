from rest_framework import serializers

from app.models import AudioRecord

class AudioRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioRecord
        fields = ['id', 'audio_file', 'transcription', 'processed', 'sent_to_openai']
        read_only_fields = ['id', 'transcription', 'processed', 'sent_to_openai']
