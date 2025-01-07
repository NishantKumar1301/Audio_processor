from django.contrib import admin # type: ignore
from .models import AudioRecord, OpenAIRequestLog, Transaction


@admin.register(AudioRecord)
class AudioRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'audio_file', 'transcription', 'processed', 'sent_to_openai', 'created_at', 'updated_at')
    search_fields = ('id', 'transcription')
    list_filter = ('processed', 'sent_to_openai', 'created_at')
    ordering = ('-created_at',)


@admin.register(OpenAIRequestLog)
class OpenAIRequestLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'audio_record', 'status', 'created_at', 'updated_at')
    search_fields = ('id', 'audio_record__id')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'selling_price', 'cost_price', 'profit', 'created_at', 'updated_at')
    search_fields = ('product_name', 'id')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
