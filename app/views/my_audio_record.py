import json
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import AudioRecord
from app.services.transaction import TransactionProcessingService
from django.shortcuts import render, get_object_or_404
from app.models import AudioRecord, OpenAIRequestLog
from django.core.paginator import Paginator

class MyAudiosView(LoginRequiredMixin, View):
    def get(self, request):
        # Fetch all audio records for the logged-in user
        user_audios = AudioRecord.objects.filter(user=request.user).order_by('-created_at')

        # Apply Pagination (Show 5 Audios per Page)
        paginator = Paginator(user_audios, 4)  
        page_number = request.GET.get('page')  # Get current page number from request
        page_obj = paginator.get_page(page_number)  # Get the correct page

        return render(request, 'my_audios.html', {'user_audios': page_obj})  # Send paginated object

    def post(self, request, audio_id):
        # Find the audio record and trigger processing
        audio_record = AudioRecord.objects.get(id=audio_id, user=request.user)
        if not audio_record.processed:
            TransactionProcessingService.process_all_audio_and_openai_requests(request.user)
        
        return redirect('my_audios')  # Redirect back after processing

class ViewAudioDetailsView(LoginRequiredMixin, View):
    def get(self, request, audio_id):
        # Fetch the specific audio record for the logged-in user
        audio_record = get_object_or_404(AudioRecord, id=audio_id, user=request.user)

        # Fetch OpenAI extracted details if available
        openai_log = OpenAIRequestLog.objects.filter(audio_record=audio_record).first()

        # Parse response_data JSON correctly
        extracted_data = {"product_name": "N/A", "cost_price": 0.00, "selling_price": 0.00}  # Default values
        if openai_log and openai_log.response_data:
            try:
                extracted_data = json.loads(openai_log.response_data)  # Convert JSON string to dictionary
            except json.JSONDecodeError:
                extracted_data = {"error": "Invalid response format"}

        context = {
            'audio_record': audio_record,
            'openai_log': extracted_data  # Pass parsed data to template
        }
        return render(request, 'audio_details.html', context)