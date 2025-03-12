from django.urls import path # type: ignore

from app.views.audio_record import AudioUploadView, AudioUploadPageView
from app.views.dashboard import dashboard_view
from app.views.auth import signup_view, login_view, logout_view
from app.views.transaction import user_transactions

urlpatterns = [
    path("", dashboard_view, name="home"), 
    path('upload_audio/', AudioUploadView.as_view(), name='upload-audio'),
    path('upload/', AudioUploadPageView.as_view(), name='upload_audio_page'),
    path("transactions/", user_transactions, name="transactions"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]