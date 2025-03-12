import logging
from app.accessors.audio_record import AudioRecordAccessor
from app.utils.whisper_util import transcribe_audio


class WhisperTranscriptionService:
    @staticmethod
    def process_unprocessed_audio_records(user):
        """
        Process unprocessed audio records for a specific user and update the transcription.
        """
        # Get the logger if defined in settings
        logger = logging.getLogger('app')

        # Fetch unprocessed audio records for the specific user
        unprocessed_records = AudioRecordAccessor.get_unprocessed_audio_records(user)
        if not unprocessed_records.exists():
            if logger:
                logger.info(f"No unprocessed audio records found for user {user.username}.")
            return

        for record in unprocessed_records:
            try:
                file_path = record.audio_file.path
                if logger:
                    logger.debug(f"Processing audio file: {file_path}")

                transcription = transcribe_audio(file_path)

                record.transcription = transcription
                AudioRecordAccessor.update_processed_status(record, transcription=transcription, processed=True)

                if logger:
                    logger.info(f"Successfully processed audio record ID: {record.id}")

            except Exception as e:
                if logger:
                    logger.error(f"Error processing record ID: {record.id} - {str(e)}")
                # Silently handle errors for now: The importance is that the application would not crash if an error is found
                pass
