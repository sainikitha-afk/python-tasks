import time
import random


def generate_thumbnail(image_id, size):
    time.sleep(1)
    return f"/thumbs/{image_id}_{size[0]}x{size[1]}.jpg"


def send_email(to, template):
    time.sleep(1)

    # Simulate failure
    if random.choice([True, False]):
        raise Exception("SMTPConnectionError")

    return "email_sent"