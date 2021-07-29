from django.contrib import admin
from .models import Organization, OrganizationProduct


@admin.register(Organization)
class OrganAdmin(admin.ModelAdmin):
    list_display = ['province', 'name', 'owner', 'employees_number', 'email', 'created_by', 'created_at']


@admin.register(OrganizationProduct)
class OrganizationProduct(admin.ModelAdmin):
    pass