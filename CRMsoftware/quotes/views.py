import weasyprint
from django.views.generic import CreateView, ListView, DetailView
from . import models
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse


class CreateQuotes(LoginRequiredMixin, CreateView):
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
        messages.success(self.request, 'پیش فاکتور ذخیره شد')
        return super(CreateQuotes, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'اطلاعات را به درستی وارد نمایید')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('quotes:quote_list')


class QuoteList(LoginRequiredMixin, ListView):
    model = models.Quote
    template_name = 'quotes/quote_item_form.html'
    paginate_by = 5


class QuoteDetail(LoginRequiredMixin, DetailView):
    model = models.Quote
    template_name = 'quotes/quote_detail.html'


class QuotePDF(LoginRequiredMixin, DetailView):
    template_name = 'quotes/quote_pdf.html'
    model = models.Quote

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        content = response.rendered_content
        pdf = weasyprint.HTML(string=content, base_url='http://127.0.0.1:8000').write_pdf()
        pdf_response = HttpResponse(content=pdf, content_type='application/pdf')
        return pdf_response
