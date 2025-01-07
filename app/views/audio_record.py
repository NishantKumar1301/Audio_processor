from rest_framework.views import APIView # type: ignore
from rest_framework.parsers import MultiPartParser, FormParser # type: ignore
from app.builders.response_builder import ResponseBuilder
from app.serializers.audio_record import AudioRecordSerializer
from app.utils.audio_utils import get_audio_duration
from app.utils.exctract_details import extract_details
from app.utils.whisper_util import transcribe_audio


class AudioUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        response = ResponseBuilder()
        serializer = AudioRecordSerializer(data=request.data)
        
        if serializer.is_valid():
            audio_record = serializer.save()
            
            try:
                file_path = audio_record.audio_file.path
                duration = get_audio_duration(file_path)
                if duration > 15:
                    audio_record.delete()
                    response.fail().bad_request_400().message("Audio duration exceeds 15 seconds.")
                    return response.get_response()
            except ValueError as e:
                audio_record.delete()
                response.fail().internal_error_500().message("Invalid audio file.")
                return response.get_response()
            
            response.success().message("Audio file uploaded successfully").result_object({
                'id': audio_record.id,
                'audio_file': audio_record.audio_file.url
            })
            return response.get_response()
        
        response.fail().bad_request_400().message("Invalid data").errors(serializer.errors)
        return response.get_response()
