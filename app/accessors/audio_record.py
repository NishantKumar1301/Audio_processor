from app.models import AudioRecord

class AudioRecordAccessor:
    @staticmethod
    def get_unprocessed_audio_records(user):
        """
        Fetch unprocessed audio records for a specific user
        """
        return AudioRecord.objects.filter(user=user, processed=False)

    @staticmethod
    def get_audio_records_not_sent_to_openai(user):
        """
        Fetch audio records that have not been sent to OpenAI for a specific user
        """
        return AudioRecord.objects.filter(user=user, sent_to_openai=False)

    @staticmethod
    def update_processed_status(audio_record, transcription, processed=True):
        """
        Update the processed status for a given audio record
        """
        audio_record.transcription = transcription
        audio_record.processed = processed
        audio_record.save()

    @staticmethod
    def update_sent_to_openai_status(audio_record, sent_to_openai=True):
        """
        Update the sent_to_openai status for a given audio record
        """
        audio_record.sent_to_openai = sent_to_openai
        audio_record.save()
