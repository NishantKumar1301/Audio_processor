from rest_framework.views import APIView  # type: ignore
from rest_framework.parsers import MultiPartParser, FormParser  # type: ignore
from app.builders.response_builder import ResponseBuilder
from app.serializers.audio_record import AudioRecordSerializer
from app.utils.audio_utils import get_audio_duration
import logging
from rest_framework.permissions import IsAuthenticated  # Add this to ensure only authenticated users can upload
from django.shortcuts import render,redirect
from django.views import View

# Get logger
logger = logging.getLogger('app')

class AudioUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can upload

    def post(self, request, *args, **kwargs):
        logger.info("Audio upload request received.")
        response = ResponseBuilder()

        # Add the user to the request data before serializing
        request.data['user'] = request.user.id  # Attach the logged-in user to the request data

        # Pass the request to the serializer context
        serializer = AudioRecordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            audio_record = serializer.save()  # The user is automatically set due to the above line
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
            
            # Render the success page with the alert and redirect
            return render(request, 'audio_upload_success.html', {
                'redirect_url': '/dashboard/'
            })

        logger.warning(f"Invalid data received: {serializer.errors}")
        response.fail().bad_request_400().message("Invalid data").errors(serializer.errors)
        return response.get_response()
    
class AudioUploadPageView(View):
    def get(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if user is not authenticated
        
        # Render the audio upload page
        return render(request, 'upload_audio.html')
