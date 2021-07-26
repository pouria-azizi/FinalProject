from django.urls import path

from . import views

urlpatterns = [
    path('create_organ/', views.CreateNewOrganization.as_view(), name='create_organ'),
    path('organ_product/', views.ShowAddEntryForm.as_view(), name='organ_product'),
]
