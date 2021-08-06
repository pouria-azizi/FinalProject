from decimal import Decimal

from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model
from django.db.models import Sum, F, Max, FloatField, ExpressionWrapper


class Quote(models.Model):
    """
    Create new Quote to use in next level
    """
    organ = models.ForeignKey('organs.Organization', on_delete=models.PROTECT)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    def __str__(self):
        return f' فاکتور شماره {self.pk} برای {self.organ}'

    def get_price_without_discount(self):
        return self.quoteitem_set.all().annotate(price_without_discount=F('qty') * F('product__price')) \
            .aggregate(Sum('price_without_discount'))['price_without_discount__sum']

    def get_price_with_discount(self):
        price_without_discount = self.quoteitem_set.all().annotate(price_without_discount=F('qty') * F('product__price')) \
            .aggregate(Sum('price_without_discount'))['price_without_discount__sum']
        price_with_discount = self.quoteitem_set.all().annotate(price_with_discount=ExpressionWrapper \
            (price_without_discount - (F('discount') / Decimal('100.0') * price_without_discount), output_field=FloatField()))
        return price_with_discount.aggregate(Max('price_with_discount'))['price_with_discount__max']

    def get_price_with_tax(self):
        price_without_discount = self.quoteitem_set.all().annotate(price_without_discount=F('qty') * F('product__price')) \
            .aggregate(Sum('price_without_discount'))['price_without_discount__sum']
        price_with_discount = self.quoteitem_set.all().annotate(price_with_discount=ExpressionWrapper(
            price_without_discount - (F('discount') / Decimal('100.0') * price_without_discount),
            output_field=FloatField())).aggregate(Max('price_with_discount'))['price_with_discount__max']
        price_with_tax = self.quoteitem_set.all().annotate(price_with_tax=ExpressionWrapper(price_with_discount + \
                                    (F('tax') / Decimal('100') * price_with_discount), output_field=FloatField()))
        return price_with_tax.aggregate(Max('price_with_tax'))['price_with_tax__max']


class QuoteItem(models.Model):
    """
    Choice quote and adding products to it
    """
    quote = models.ForeignKey('quotes.Quote', on_delete=models.PROTECT)
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    discount = models.FloatField(default=0)
    tax = models.FloatField(default=5)

    def __str__(self):
        return f'{self.quote}'


class Email(models.Model):
    created_at = jmodels.jDateTimeField(auto_now_add=True,)
    # email_sender = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    email_receiver = models.EmailField()
    status = models.BooleanField(default=False)
