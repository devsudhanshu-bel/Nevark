import uuid
from datetime import datetime


def generate_id():

    return str(uuid.uuid4())


def current_timestamp():

    return str(datetime.now())


def clean_text(text: str):

    return text.strip()
