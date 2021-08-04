from django import forms
from .models import QuoteItem


class QuoteForm(forms.ModelForm):

    class Meta:
        model = QuoteItem
        fields = [
            'quote',
            'product',
            'qty',
            'discount',
            'tax',
        ]
