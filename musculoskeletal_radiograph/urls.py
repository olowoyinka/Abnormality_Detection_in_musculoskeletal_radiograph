"""musculoskeletal_radiograph URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from musculoskeletal_radiograph_app import views
from django.conf.urls.static import static
from musculoskeletal_radiograph import settings

urlpatterns = [
    path('', views.HomePage, name="home"),
    path('admin/', admin.site.urls),
    path('patient/register', views.CreatePatient, name="register_patient"),
    path('patient', views.GetAllPatient, name="patient"),
    path('patient/<str:patient_id>', views.GetPatient, name="get_patient"),
    path('patient/<str:patient_id>/radiograph/<str:radiograph_id>', views.GetRadiograph, name="get_radiograph"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
