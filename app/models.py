from django.db import models # type: ignore
from app.utils.utils import get_char_uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, max_length=100, db_index=True, editable=False, default=get_char_uuid)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AudioRecord(BaseModel):
    audio_file = models.FileField(upload_to='user_audio/')
    transcription = models.TextField(blank=True, null=True)
    processed = models.BooleanField(default=False)
    sent_to_openai = models.BooleanField(default=False)

    def __str__(self):
        return f"AudioRecord {self.id}"


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
