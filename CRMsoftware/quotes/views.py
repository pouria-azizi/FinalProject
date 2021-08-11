import weasyprint
from django.views.generic import CreateView, ListView, DetailView
from . import models, tasks, forms
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.core import mail
from django.utils.html import strip_tags
from .models import Email
from rest_framework.exceptions import NotAuthenticated
from django.http import JsonResponse, HttpResponse

class CreateItemQuotes(LoginRequiredMixin, CreateView):
    """
    Add item to quote
    """
    template_name = 'quotes/quote_form.html'
    model = models.QuoteItem
    fields = [
        'quote',
        'product',
        'qty',
        'discount'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = models.Quote.objects.all()
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'فاکتور ذخیره شد')
        return super(CreateItemQuotes, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'اطلاعات نادرست است')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('quotes:quote_list')


class CreateQuotes(LoginRequiredMixin, CreateView):
    """
    Create quote
    """
    template_name = 'quotes/new_quote.html'
    model = models.Quote
    fields = [
        'organ',
    ]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'پیش فاکتور جدید ایجاد شد')
        return super(CreateQuotes, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'اطلاعات نادرست است')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('quotes:create_quote')


class QuoteList(LoginRequiredMixin, ListView):
    """
    Show the list of quotes
    """
    model = models.Quote
    template_name = 'quotes/quote_item_form.html'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise NotAuthenticated('You need to be logged on.')
        return models.Quote.objects.filter(created_by=self.request.user)


class QuoteDetail(LoginRequiredMixin, DetailView):
    """
    Show the detail of single quote
    """
    model = models.Quote
    template_name = 'quotes/quote_detail.html'
    extra_context = {'quote_pk': models.QuoteItem.quote}

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise NotAuthenticated('You need to be logged on.')
        return models.Quote.objects.filter(created_by=self.request.user)


class QuotePDF(LoginRequiredMixin, DetailView):
    """
    Rendering quote to PDF
    """
    template_name = 'quotes/quote_pdf.html'
    model = models.Quote

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        content = response.rendered_content
        pdf = weasyprint.HTML(string=content, base_url='http://127.0.0.1:8000').write_pdf()
        pdf_response = HttpResponse(content=pdf, content_type='application/pdf')
        return pdf_response

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise NotAuthenticated('You need to be logged on.')
        return models.Quote.objects.filter(created_by=self.request.user)


@require_http_methods(["GET"])
@login_required
def send_email_to_organs(request, pk):
    try:

        html_message = render_to_string('quotes/quote_pdf.html', context={'object': models.Quote.objects.get(pk=pk, created_by=request.user)})
        plain_message = strip_tags(html_message)
        to = models.Quote.objects.get(pk=pk).organ.email
        email_sender1 = request.user.username
        # mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        tasks.send_email.delay(plain_message, email_sender1, [to], html_message=html_message)
        messages.success(request, 'ایمیل با موفقیت ارسال شد')
        return redirect('quotes:quote_list')

    except:

        messages.error(request, 'ایمیل ارسال نشد')
        return redirect('quotes:quote_list')
