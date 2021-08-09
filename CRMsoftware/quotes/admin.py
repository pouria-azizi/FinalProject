from django.contrib import admin
from .models import Quote, QuoteItem, Email


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    inlines = (
        QuoteItemInline,
    )


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    model = Email
    list_display = ['email_sender', 'email_receiver', 'status', 'created_at']
    list_filter = ['email_sender', 'email_receiver', 'status']
