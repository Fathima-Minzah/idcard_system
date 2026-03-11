import uuid
import qrcode
from io import BytesIO
from django.db import models
from django.core.files import File
from django.conf import settings

class SystemSettings(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    value = models.TextField()
    company_name = models.CharField(
        max_length=255,
        verbose_name="Company Name",
        help_text="Name of the company the implementation is for",
        blank=True,
        null=True
    )

    company_site = models.CharField(
        max_length=255,
        verbose_name="Company Website",
        blank=True,
        null=True
    )

    company_logo = models.ImageField(
        upload_to="company_logo/",
        verbose_name="Company Logo",
        help_text="Upload the company logo",
        blank=True,
        null=True
    )

    class Meta:
        db_table = "system_settings"
        verbose_name = "System Setting"
        verbose_name_plural = "System Settings"

    def __str__(self):
        return self.name       
    
class Employee(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name="UUID")
    employee_id = models.CharField(max_length=20, unique=True, verbose_name="Employee ID")
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    
    # Additional personal info
    #nic = models.CharField(max_length=20, null=True, verbose_name="NIC")  # National ID
    nic = models.CharField(max_length=20, unique=True, null=True, verbose_name="NIC")  # remove unique=True temporarily
    address = models.TextField()
    designation = models.CharField(max_length=100, default="")
    staff_mobile = models.CharField(max_length=20, default="", verbose_name="Staff Mobile")
    photo = models.ImageField(upload_to='employee_photos/')
    qr_link = models.URLField(blank=True, null=True, verbose_name="QR Link")
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True, editable=False)
    is_active = models.BooleanField(default=True)

    manager_name = models.CharField(max_length=100, verbose_name="Direct Report's Name", default="")
    manager_mobile = models.CharField(max_length=20, verbose_name="Direct Report's Mobile Number", default="")

    class Meta:
        verbose_name = "Staff Verification"
        verbose_name_plural = "Staff Verification"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
      if not self.qr_code or not self.qr_link:
        self.generate_qr()
      super().save(*args, **kwargs)

    def generate_qr(self):
      #base_url = "http://127.0.0.1:8000/staff_verification/"
      base_url = f"{settings.SITE_URL}/staff_verification/"
      qr_content = f"{base_url}{self.uuid}"

    # Save link to database
      self.qr_link = qr_content

    # Generate QR image
      qr_img = qrcode.make(qr_content)

      buffer = BytesIO()
      qr_img.save(buffer, format='PNG')
      buffer.seek(0)

      file_name = f"{self.uuid}.png"
      self.qr_code.save(file_name, File(buffer), save=False) 
