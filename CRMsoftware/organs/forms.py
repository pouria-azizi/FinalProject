from django import forms
from . import models


class EntryOrganizationForm(forms.ModelForm):
    class Meta:
        model = models.Organization
        fields = [
            'province',
            'name',
            'organization_phone',
            'employees_number',
            'owner',
            'email',
            'owner_phone',
            'organization_product',
        ]
