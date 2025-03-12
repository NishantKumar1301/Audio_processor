from app.services.whisper_transcription import WhisperTranscriptionService
from app.services.open_ai import OpenAIService

class TransactionProcessingService:
    @staticmethod
    def process_all_audio_and_openai_requests(user):
        """
        Unified function to:
        1. Process unprocessed audio records and update transcriptions.
        2. Initialize OpenAI request logs for audio records not sent to OpenAI.
        3. Process pending OpenAI requests and create/update transactions.
        """
        # Step 1: Process unprocessed audio records for the specific user
        WhisperTranscriptionService.process_unprocessed_audio_records(user)

        # Step 2: Initialize OpenAI request logs
        OpenAIService.initialize_openai_requests(user)

        # Step 3: Process OpenAI requests and create/update transactions
        OpenAIService.process_pending_requests_and_create_transactions()
