from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
# from products.models import Product # noqa

phone_regex = RegexValidator(regex='^0[0-9]{2,}[0-9]{7,}$', message='phone number invalid')


class OrganizationProduct(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Organization(models.Model):
    province = models.CharField(max_length=100)
    name = models.CharField(max_length=150)
    organization_phone = models.CharField(validators=[phone_regex], max_length=11)
    employees_number = models.CharField(max_length=10000)
    owner = models.CharField(max_length=150)
    email = models.EmailField()
    owner_phone = models.CharField(validators=[phone_regex], max_length=11)
    organization_product = models.ManyToManyField(OrganizationProduct)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'created_by'], name='UniqueOrgan')
        ]

    # def __str__(self):
    #     return f'{self.organization_product.name}'

    # def __getitem__(self, item):
    #     self.re_p = Organization.objects.all()
    #     # self.related_products = self.re_p.organization_set.all()
    #     rr = OrganizationProduct.objects.filter(related_product__in=self.re_p)
    #     return rr

    # def __getitem__(self, item):
    #     products = OrganizationProduct.objects.all()
    #     qs = products.objects.filter(related_item__in=self.organization_product)
    #     return qs

    def related_item(self):
        products = set()
        for product in self.organization_product.all():
            products = set(product.get_name)
        return list(products)
