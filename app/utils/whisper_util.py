# import whisper

# def transcribe_audio(file_path, language = "en"):
#     """
#     Transcribe audio using OpenAI's Whisper.
#     :param file_path: Path to the audio file to transcribe
#     :return: Transcription text or error message
#     """
#     try:
#         model = whisper.load_model("small")
#         result = model.transcribe(file_path, language=language)
#         return result.get('text', '')
#     except Exception as e:
#         return str(e)


import whisper
import ffmpeg

# Load the Whisper model **once** at the start
whisper_model = whisper.load_model("base")  # "tiny" or "base" is recommended for low memory usage

def preprocess_audio(input_file, output_file="temp_converted.wav"):
    """ Convert audio to 16kHz mono WAV format to reduce size """
    try:
        ffmpeg.input(input_file).output(output_file, ac=1, ar=16000).run(overwrite_output=True, quiet=True)
        return output_file
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None

def transcribe_audio(file_path, language="en"):
    """
    Transcribe audio using OpenAI's Whisper with optimized performance.
    
    :param file_path: Path to the audio file to transcribe
    :param language: Language of the audio (default: English)
    :return: Transcription text or error message
    """
    try:
        # Convert audio to a smaller format (16kHz mono WAV)
        processed_audio = preprocess_audio(file_path)
        if not processed_audio:
            return "Audio preprocessing failed"

        # Use the **preloaded** model instead of loading every time
        result = whisper_model.transcribe(processed_audio, language=language)
        return result.get("text", "Transcription failed")
    except Exception as e:
        return str(e)
