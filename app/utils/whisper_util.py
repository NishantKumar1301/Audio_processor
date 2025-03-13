import whisper

def transcribe_audio(file_path, language = "en"):
    """
    Transcribe audio using OpenAI's Whisper.
    :param file_path: Path to the audio file to transcribe
    :return: Transcription text or error message
    """
    try:
        model = whisper.load_model("small")
        result = model.transcribe(file_path, language=language)
        return result.get('text', '')
    except Exception as e:
        return str(e)
