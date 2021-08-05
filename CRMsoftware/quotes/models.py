from decimal import Decimal

from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from django.db.models import Sum, F, Max, FloatField, ExpressionWrapper


class Quote(models.Model):
    organ = models.ForeignKey('organs.Organization', on_delete=models.PROTECT)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f' فاکتور شماره {self.pk} برای {self.organ}'

    def get_grand_total(self):
        """
        Returns grand total of Order
        """
        price = self.quoteitem_set.all().annotate(price=F('product__price') * F('qty')).aggregate(Max('price'))[
            'price__max']
        return price

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
    quote = models.ForeignKey('quotes.Quote', on_delete=models.PROTECT)
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    discount = models.FloatField(default=0)
    tax = models.FloatField(default=5)

    def __str__(self):
        return f'Quote #{self.pk} for {self.quote}'


    # def calculate_price_without_discount(self):
    #     price_without_discount = self.qty * self.product.price
    #     return price_without_discount
    #
    # def calculate_price_with_discount(self):
    #     total_discount = float(self.calculate_price_without_discount()) * self.discount / 100
    #     price_with_discount = float(self.calculate_price_without_discount()) - total_discount
    #     return price_with_discount
    #
    # def calculate_price_with_tax(self):
    #     total_tax = float(self.calculate_price_with_discount()) * self.tax / 100
    #     price_with_tax = float(self.calculate_price_with_discount()) + total_tax
    #     return price_with_tax

#
# class Email(models.Model):
#     """
#     Email configurations and saving email histories
#     """
#     created_by = models.ForeignKey(User, on_delete=models.PROTECT)
#     created_at = jmodels.jDateTimeField(auto_now_add=True)
#     status = models.BooleanField(default=True)
#     email = models.CharField(max_length=50)
