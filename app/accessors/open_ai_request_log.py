from app.accessors.audio_record import AudioRecordAccessor
from app.models import OpenAIRequestLog


class OpenAIRequestLogAccessor:
    @staticmethod
    def create_initial_entries_for_openai_request():
        audio_records = AudioRecordAccessor.get_audio_records_not_sent_to_openai()
        for audio_record in audio_records:
            # Create OpenAIRequestLog with status PENDING
            OpenAIRequestLog.objects.create(
                audio_record=audio_record,
                request_data="",
                response_data="",
                status="PENDING"
            )
            # Mark the audio record as sent to OpenAI
            AudioRecordAccessor.update_sent_to_openai_status(audio_record)

    @staticmethod
    def get_pending_requests():
        return OpenAIRequestLog.objects.filter(status="PENDING")

    @staticmethod
    def update_request_log_status(request_log, request_data, response_data, status):
        request_log.request_data = request_data
        request_log.response_data = response_data
        request_log.status = status
        request_log.save()
