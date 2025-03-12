from django.db import models # type: ignore
from app.utils.utils import get_char_uuid
from django.contrib.auth.models import User
import os

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, max_length=100, db_index=True, editable=False, default=get_char_uuid)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

def default_profile_pic():
    """Returns a fixed default profile picture from the media folder."""
    return "dp.jpeg"  # Ensure this image exists in media/profile_pics/profile.png


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)  # Auto-updates on profile changes

    def __str__(self):
        return self.user.username

    def get_profile_pic_url(self):
        """Returns the uploaded profile picture URL or default image"""
        if self.profile_pic:
            return self.profile_pic.url
        return "/media/dp.jpeg"  # Ensure this file exists inside media/

# models.py
class AudioRecord(BaseModel):
    audio_file = models.FileField(upload_to='user_audio/')
    transcription = models.TextField(blank=True, null=True)
    processed = models.BooleanField(default=False)
    sent_to_openai = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="audio_records")  # non-nullable

    def __str__(self):
        return f"AudioRecord {self.id} for {self.user.username}"



class OpenAIRequestLog(BaseModel):
    audio_record = models.ForeignKey(AudioRecord, on_delete=models.CASCADE, related_name='openai_requests')
    request_data = models.TextField(blank=True, null=True)
    response_data = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=(
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed')
    ), default='PENDING')

    def __str__(self):
        return f"OpenAIRequestLog {self.id}"


class Transaction(BaseModel):
    openai_request = models.OneToOneField(OpenAIRequestLog, on_delete=models.CASCADE, related_name='transaction')
    product_name = models.CharField(max_length=255, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def calculate_profit(self):
        if self.selling_price and self.cost_price:
            self.profit = self.selling_price - self.cost_price
            self.save()

    def __str__(self):
        return f"Transaction {self.id} - {self.product_name or 'Unknown Product'}"
