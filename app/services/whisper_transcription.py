import logging
from app.accessors.audio_record import AudioRecordAccessor
from app.utils.whisper_util import transcribe_audio


class WhisperTranscriptionService:
    @staticmethod
    def process_unprocessed_audio_records():
        # Get the logger if defined in settings
        logger = logging.getLogger('app')

        unprocessed_records = AudioRecordAccessor.get_unprocessed_audio_records()
        if not unprocessed_records.exists():
            if logger:
                logger.info("No unprocessed audio records found.")
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
                # Silently handle errors for now : Its importance is that the application would not be crashed if the error is found 
                pass
