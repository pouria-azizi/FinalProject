from django.contrib import admin
from .models import Product

#
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image', 'name', 'slug', 'price', 'available', 'created']
    list_filter = ['available', 'created', 'slug']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
