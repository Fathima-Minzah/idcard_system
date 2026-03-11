from django.contrib.admin import AdminSite
from django.apps import apps


class StaffAdminSite(AdminSite):
    site_header = "PRAGICTS | STAFF VERIFICATION PLATFORM ADMIN"
    site_title = "Employee Admin Portal"
    index_title = ""
    site_url = "https://pragicts.com/"

    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        # Apps we want to completely hide
        apps_to_hide = ["otp_email", "otp_static", "otp_totp", "two_factor"]

        filtered_app_list = []
        for app in app_list:
            if app["app_label"] not in apps_to_hide:
                filtered_app_list.append(app)

        return filtered_app_list


staff_admin_site = StaffAdminSite(name="staff_admin")