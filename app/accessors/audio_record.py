from app.models import AudioRecord


class AudioRecordAccessor:
    @staticmethod
    def get_unprocessed_audio_records():
        return AudioRecord.objects.filter(processed=False)

    @staticmethod
    def get_audio_records_not_sent_to_openai():
        return AudioRecord.objects.filter(sent_to_openai=False)

    @staticmethod
    def update_processed_status(audio_record, transcription, processed=True):
        audio_record.transcription = transcription
        audio_record.processed = processed
        audio_record.save()

    @staticmethod
    def update_sent_to_openai_status(audio_record, sent_to_openai=True):
        audio_record.sent_to_openai = sent_to_openai
        audio_record.save()
