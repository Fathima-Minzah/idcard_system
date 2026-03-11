from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee
from .utils import generate_qr

@receiver(post_save, sender=Employee)
def create_qr(sender, instance, created, **kwargs):
    if created and not instance.qr_code:
        qr_path = generate_qr(instance)
        instance.qr_code = qr_path
        instance.save()
