from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels
from django.core.validators import FileExtensionValidator


class Product(models.Model):
    """
    Products to be sold to organizations
    """
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=False)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    file = models.FileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    follow_product = models.ManyToManyField('organs.OrganizationProduct')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])

    # def get_related_product(self):
    #     related = OrganizationProduct.objects.all()
    #     return Organization.objects.filter(organization_product__in=related).distinct()
