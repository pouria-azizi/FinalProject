from django.urls import path, include

from . import views
from rest_framework.routers import DefaultRouter

router2 = DefaultRouter()
router2.register('phones', views.OrgansListApi)

urlpatterns = [
    path('create_organ/', views.CreateNewOrganization.as_view(), name='create_organ'),
    # path('organ_product/', views.ShowAddEntryForm.as_view(), name='organ_product'),
    path('organ_list/', views.OrgansList.as_view(), name='organ_list'),
    path('organ_detail/<int:pk>', views.OrgansDetail.as_view(), name='organ_detail'),
    path('organ_edit/<int:pk>', views.EditOrgan.as_view(), name='organ_edit'),
    path('organ_product/', views.OrganizationNewProduct.as_view(), name='organ_product'),
    path('api/v0/', include(router2.urls)),
]
