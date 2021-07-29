from django import forms
from . import models


class EntryOrganizationForm(forms.ModelForm):
    class Meta:
        model = models.Organization
        fields = [
            'organization_product',
        ]
