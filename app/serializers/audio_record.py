from rest_framework import serializers
from app.models import AudioRecord

class AudioRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioRecord
        fields = ['audio_file', 'transcription', 'processed', 'sent_to_openai', 'user']

    def create(self, validated_data):
        # Access the user from the request context
        user = self.context['request'].user  # Get the logged-in user
        validated_data['user'] = user  # Add the user to the validated data
        return super().create(validated_data)  # Proceed with saving the instance
