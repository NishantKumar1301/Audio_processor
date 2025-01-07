from app.accessors.audio_record import AudioRecordAccessor
from app.utils.whisper_util import transcribe_audio


class WhisperTranscriptionService:
    @staticmethod
    def process_unprocessed_audio_records():
        unprocessed_records = AudioRecordAccessor.get_unprocessed_audio_records()
        if not unprocessed_records.exists():
            return

        for record in unprocessed_records:
            try:
                file_path = record.audio_file.path
                transcription = transcribe_audio(file_path)

                record.transcription = transcription
                AudioRecordAccessor.update_processed_status(record, transcription=transcription, processed=True)
            except Exception as e:
                # Silently handle errors for now: BAD CODE
                pass
