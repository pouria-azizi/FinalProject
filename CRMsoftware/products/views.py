from . import models
from django.views.generic import ListView, DetailView, CreateView


class ProductList(ListView):
    """
    Show the list of products
    """
    model = models.Product

    paginate_by = 8
    template_name = 'products/list.html'


class ProductDetail(DetailView):
    """
    Show the detail of single product
    """
    model = models.Product
    template_name = 'products/detail.html'
