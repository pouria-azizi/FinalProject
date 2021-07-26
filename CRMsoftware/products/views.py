from django.shortcuts import render, get_object_or_404

from . import models
from .models import Category, Product
from django.views.generic import ListView, DetailView, CreateView


class ProductList(ListView):
    model = models.Product

    paginate_by = 8
    template_name = 'products/list.html'


class CategoryList(ListView):
    model = models.Category
    template_name = 'products/list.html'


# def product_detail(request, id, slug):
#     product = get_object_or_404(Product, id=id, slug=slug, available=True)
#     return render(request, 'products/detail.html', {'product': product})


class ProductDetail(DetailView):
    model = models.Product
    template_name = 'products/detail.html'
