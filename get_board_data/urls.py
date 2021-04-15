from django.urls import path
from . import views

urlpatterns = [
    path('generate_board_certificate/<slug:slug>', views.generate_board_certificate, name="generate_board_certificate"),
    path('board/<slug:slug>', views.display_board_certificate, name="display_board_certificate"),
    path('convert_board_certificate_to_pdf/<slug:slug>', views.convert_certificate_to_pdf, name="convert_certificate_to_pdf"),
    path('board_profile_image/<slug:slug>', views.board_profile_image, name="board_profile_image")
]