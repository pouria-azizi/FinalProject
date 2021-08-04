from django.contrib import admin
from .models import Quote, QuoteItem


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    inlines = (
        QuoteItemInline,
    )
