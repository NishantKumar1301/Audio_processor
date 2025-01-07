import subprocess

def get_audio_duration(file_path):
    """
    Get the duration of an audio file using ffprobe.
    :param file_path: Path to the audio file
    :return: Duration in seconds
    """
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return float(result.stdout.strip())
    except Exception as e:
        raise ValueError("Unable to determine audio duration") from e
