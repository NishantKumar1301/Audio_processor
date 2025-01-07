from django.urls import path # type: ignore

from app.views.audio_record import AudioUploadView

urlpatterns = [
    path('upload_audio/', AudioUploadView.as_view(), name='upload-audio'),
]