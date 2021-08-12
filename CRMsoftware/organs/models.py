from django.core.validators import RegexValidator
from django.db import models
from django_jalali.db import models as jmodels
from products.models import Product # noqa
from django.contrib.auth import get_user_model


phone_regex = RegexValidator(regex='^0[0-9]{2,}[0-9]{7,}$', message='phone number invalid')


class OrganizationProduct(models.Model):
    """
    Products of organs
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Organization(models.Model):
    """
    Model to save the specifications of organs
    """
    province = models.CharField(max_length=100)
    name = models.CharField(max_length=150)
    organization_phone = models.CharField(validators=[phone_regex], max_length=11)
    employees_number = models.PositiveIntegerField(default=1)
    owner = models.CharField(max_length=150)
    email = models.EmailField()
    owner_phone = models.CharField(validators=[phone_regex], max_length=11)
    organization_product = models.ManyToManyField('OrganizationProduct')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'created_by'], name='UniqueOrgan')
        ]

    def __str__(self):
        return self.name

    # def get_related_product(self):
    #     related = OrganizationProduct.objects.all()
    #     return Product.objects.filter(follow_product__in=related).distinct()


class FollowUp(models.Model):
    description = models.TextField(blank=True)
    organ = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created = jmodels.jDateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.organ}'
    #
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['description', 'organ'], name='UniqueFollowUp')
    #     ]