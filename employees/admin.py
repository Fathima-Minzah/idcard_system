from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Employee
from django.contrib.auth.models import Group, User
from django.apps import apps
from django.contrib import admin
from django.utils.html import format_html
from .models import Employee

from django_otp.plugins.otp_static.models import StaticDevice, StaticToken
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_email.models import EmailDevice as OTPEmailDevice
from .models import SystemSettings


admin.site.site_header = "PRAGICTS | STAFF VERIFICATION PLATFORM ADMIN"
admin.site.site_title = "Employee Admin Portal"
admin.site.index_title = ""

admin.site.site_url = "https://pragicts.com/"

# Optional: Unregister default groups
admin.site.unregister(Group)

# Unregister 2FA related models

models_to_hide = [
    ("otp_totp", "TOTPDevice"),
    ("otp_static", "StaticDevice"),
    ("otp_static", "StaticToken"),
    ("otp_email", "EmailDevice"),
    ("two_factor", "PhoneDevice"),
]

for app_label, model_name in models_to_hide:
    try:
        model = apps.get_model(app_label, model_name)
        admin.site.unregister(model)
    except Exception:
        pass

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid',  "qr_preview",)
    list_display = ("employee_id", "first_name", "last_name","uuid", "qr_preview")

    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html(
                '''
                <div style="text-align:center;">
                    <img src="{}" width="200"/><br><br>
                    <a href="{}" download style="
                        background:#D32F2F;
                        padding:8px 15px;
                        color:white;
                        text-decoration:none;
                        border-radius:5px;
                    ">
                        Download QR Code
                    </a>
                </div>
                ''',
                obj.qr_code.url,
                obj.qr_code.url
            )
        return "No QR Code"

    qr_preview.short_description = "QR Code"


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ("name", "value")    


