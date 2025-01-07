import uuid


def get_char_uuid(length: int = None) -> str:
    id = uuid.uuid4().hex
    return id[:length]