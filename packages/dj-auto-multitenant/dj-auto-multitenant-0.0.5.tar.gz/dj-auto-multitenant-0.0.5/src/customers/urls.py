from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('tenant/create/',views.CreateTenantView.as_view()),
]
