from decimal import Decimal

from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from django.db.models import Sum, F


class Quote(models.Model):
    organ = models.ForeignKey('organs.Organization', on_delete=models.PROTECT)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f' پیش فاکتور {self.pk}# برای {self.organ}'

    def get_total_qty(self):
        """
        Sums total qty of related order items in PYTHON
        (which is inefficient)
        """
        return self.quoteitem_set.aggregate(Sum('product__price')).get('product__price__sum', 0)

    # def get_item_rows(self):
    #     return self.quoteitem_set.count()

    def get_grand_total(self):
        """
        Returns grand total of Order
        """
        # Using aggregate and annotate
        return self.quoteitem_set.all().annotate(grand_total=F('qty') * F('price')) \
            .aggregate(Sum('grand_total'))['grand_total__sum']

    def get_price_without_discount(self):
        return self.quoteitem_set.all().annotate(price_without_discount=F('product__price') * F('qty')).aggregate(Sum('price_without_discount'))['price_without_discount__sum']

    def get_price_with_discount(self):
        total_discount = self.quoteitem_set.all().annotate(total_discount=self.get_price_without_discount() * F('discount') / Decimal('100'))
        price_with_discount = self.get_price_without_discount() - total_discount
        return price_with_discount

    def get_price_with_tax(self):
        total_tax = self.quoteitem_set.all().annotate(total_tax=self.get_price_with_discount() * F('tax') / Decimal('100'))
        price_with_tax = self.get_price_with_discount() + total_tax
        return price_with_tax


class QuoteItem(models.Model):
    quote = models.ForeignKey('quotes.Quote', on_delete=models.PROTECT)
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    discount = models.FloatField(default=0)
    tax = models.FloatField(default=5)

    def __str__(self):
        return f'{self.quote}'


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
