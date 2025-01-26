import logging
from app.models import AudioRecord

# Initialize logger
logger = logging.getLogger('app')
class AudioRecordAccessor:
    @staticmethod
    def get_unprocessed_audio_records():
        logger.info("Fetching unprocessed audio records.")
        return AudioRecord.objects.filter(processed=False)

    @staticmethod
    def get_audio_records_not_sent_to_openai():
        logger.info("Fetching audio records not sent to OpenAI.")
        return AudioRecord.objects.filter(sent_to_openai=False)

    @staticmethod
    def update_processed_status(audio_record, transcription, processed=True):
        logger.info(f"Updating processed status for AudioRecord {audio_record.id}.")
        audio_record.transcription = transcription
        audio_record.processed = processed
        audio_record.save()
        logger.info(f"Processed status updated for AudioRecord {audio_record.id}.")

    @staticmethod
    def update_sent_to_openai_status(audio_record, sent_to_openai=True):
        logger.info(f"Updating sent-to-OpenAI status for AudioRecord {audio_record.id}.")
        audio_record.sent_to_openai = sent_to_openai
        audio_record.save()
        logger.info(f"Sent-to-OpenAI status updated for AudioRecord {audio_record.id}.")
