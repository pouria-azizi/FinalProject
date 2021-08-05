from .models import QuoteItem
from django.forms import modelformset_factory


QuoteItemForm = modelformset_factory(QuoteItem, fields=('quote', 'product', 'qty', 'discount'), extra=1)
