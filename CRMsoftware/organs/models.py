from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

from products.models import Product

phone_regex = RegexValidator(regex='^0[0-9]{2,}[0-9]{7,}$', message='phone number invalid')


class OrganizationProduct(models.Model):
    name = models.ManyToManyField(Product)


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
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'created_by'], name='UniqueOrgan')
        ]



    # def __str__(self):
    #     return self.name
