from django.contrib import admin
from .models import Organization


@admin.register(Organization)
class OrganAdmin(admin.ModelAdmin):
    list_display = ['province', 'name', 'owner', 'employees_number', 'email', 'created_by', 'created_at']
