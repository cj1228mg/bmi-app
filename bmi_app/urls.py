from django.urls import path

from . import views

app_name = "bmi_app"

urlpatterns = [
    path("", views.index, name='index'),
    path("about-bmi", views.about_bmi, name='about_bmi'),
]