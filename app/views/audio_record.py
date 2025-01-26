from rest_framework.views import APIView  # type: ignore
from rest_framework.parsers import MultiPartParser, FormParser  # type: ignore
from app.builders.response_builder import ResponseBuilder
from app.serializers.audio_record import AudioRecordSerializer
from app.utils.audio_utils import get_audio_duration
from app.utils.exctract_details import extract_details
from app.utils.whisper_util import transcribe_audio
import logging

# Get logger
logger = logging.getLogger('app')
class AudioUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        logger.info("Audio upload request received.")
        response = ResponseBuilder()
        serializer = AudioRecordSerializer(data=request.data)

        if serializer.is_valid():
            audio_record = serializer.save()
            logger.info(f"AudioRecord {audio_record.id} saved successfully.")

            try:
                file_path = audio_record.audio_file.path
                logger.debug(f"Processing audio file: {file_path}")
                duration = get_audio_duration(file_path)
                logger.info(f"Audio file duration: {duration} seconds")

                if duration > 15:
                    audio_record.delete()
                    logger.warning(f"AudioRecord {audio_record.id} deleted due to exceeding duration limit (15 seconds).")
                    response.fail().bad_request_400().message("Audio duration exceeds 15 seconds.")
                    return response.get_response()
            except ValueError as e:
                audio_record.delete()
                logger.error(f"Invalid audio file: {e}")
                response.fail().internal_error_500().message("Invalid audio file.")
                return response.get_response()

            logger.info(f"AudioRecord {audio_record.id} processed successfully.")
            response.success().message("Audio file uploaded successfully").result_object({
                'id': audio_record.id,
                'audio_file': audio_record.audio_file.url
            })
            return response.get_response()

        logger.warning(f"Invalid data received: {serializer.errors}")
        response.fail().bad_request_400().message("Invalid data").errors(serializer.errors)
        return response.get_response()
