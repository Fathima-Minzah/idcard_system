import qrcode
from django.conf import settings
import os

def generate_qr(employee):
    qr_data = f"{settings.SITE_URL}/employee/{employee.uuid}/"

    qr = qrcode.make(qr_data)
    file_path = os.path.join(
        settings.MEDIA_ROOT,
        f"qr_codes/{employee.uuid}.png"
    )

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    qr.save(file_path)

    return f"qr_codes/{employee.uuid}.png"
