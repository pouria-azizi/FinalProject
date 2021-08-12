from .models import QuoteItem
from django.forms import modelformset_factory


QuoteItemFormSet = modelformset_factory(QuoteItem, fields=('product', 'qty', 'discount'), extra=1)
