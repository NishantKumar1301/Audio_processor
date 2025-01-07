from app.services.open_ai import OpenAIService
from app.services.whisper_transcription import WhisperTranscriptionService


class TransactionProcessingService:
    @staticmethod
    def process_all_audio_and_openai_requests():
        """
        Unified function to:
        1. Process unprocessed audio records and update transcriptions.
        2. Initialize OpenAI request logs for audio records not sent to OpenAI.
        3. Process pending OpenAI requests and create/update transactions.
        """
        # Step 1: Process unprocessed audio records
        WhisperTranscriptionService.process_unprocessed_audio_records()

        # Step 2: Initialize OpenAI request logs
        OpenAIService.initialize_openai_requests()

        # Step 3: Process OpenAI requests and create/update transactions
        OpenAIService.process_pending_requests_and_create_transactions()
