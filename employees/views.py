from django.shortcuts import render
import os

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Employee
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Employee
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

class TwoFactorLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('two_factor:login')  # Redirect to MFA login
        return super().get(request, *args, **kwargs)

def index(request):
    return render(request, 'index.html')  

def employee_profile(request, uuid):
    employee = get_object_or_404(Employee, uuid=uuid, is_active=True)
    return render(request, "employees/employee_profile.html", {"employee": employee})


def generate_id_card_pdf(request, uuid):
    employee = Employee.objects.get(uuid=uuid)

    template = get_template('employees/id_card.html')
    html = template.render({'employee': employee})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{employee.employee_id}.pdf"'

    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
        link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse("PDF generation error")

    return response

def link_callback(uri, rel):
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = finders.find(uri.replace(settings.STATIC_URL, ""))
    else:
        return uri

    if not os.path.isfile(path):
        raise Exception(f"Media file not found: {path}")

    return path
