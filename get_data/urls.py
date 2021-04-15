from django.urls import path
from . import views

urlpatterns = [
    path('generate_certificate/<slug:slug>', views.generate_certificate, name="generate_certificate"),
    path('events/<slug:slug>', views.display_certificate, name="display_certificate"),
    path('convert_to_pdf/<slug:slug>', views.convert_certificate_to_pdf, name="convert_certificate_to_pdf") 
]