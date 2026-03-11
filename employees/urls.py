
from .views import employee_profile
from .views import generate_id_card_pdf
from .views import TwoFactorLoginView 
from django.urls import path, include

urlpatterns = [
    path('staff_verification/<uuid:uuid>/', employee_profile, name='employee_profile'),
    path('employee/id-card/<uuid:uuid>/', generate_id_card_pdf, name='id_card_pdf'),
]
