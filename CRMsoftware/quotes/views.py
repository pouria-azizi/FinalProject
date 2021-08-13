import weasyprint
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from . import models, tasks, forms
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
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
from django.utils.decorators import method_decorator
from organs.models import Organization # noqa
from django.urls import reverse_lazy


@method_decorator(csrf_exempt, name='dispatch')
class CreateQuotes(LoginRequiredMixin, CreateView):
    """
        create quotes for organs, using formset
    """
    template_name = 'quotes/new_quote.html'

    def get_context_data(self, **kwargs):
        formset = forms.QuoteItemFormSet(queryset=models.QuoteItem.objects.none())
        organizations = Organization.objects.filter(created_by=self.request.user)
        return {
            'formset': formset,
            'organizations': organizations,
        }

    def post(self, *args, **kwargs):
        formset = forms.QuoteItemFormSet(data=self.request.POST)
        if formset.is_valid() and self.request.POST['organization']:
            try:
                organization = Organization.objects.get(pk=self.request.POST['organization'], created_by=self.request.user)
                quote = models.Quote.objects.create(created_by=self.request.user, organ=organization)

                for form in formset:
                    form.instance.quote = quote
                    form.save()
                messages.success(self.request, 'فاکتور با موفقیت صادر شد')
                return redirect('quotes:quote_list')
            except:
                messages.error(self.request, 'لطفا اطلاعات درست را وارد نمایید')
                return redirect('quotes:quote_list')
        else:
            messages.error(self.request, 'لطفا اطلاعات درست را وارد نمایید')
            return redirect('quotes:quote_list')


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
        return models.Quote.objects.filter(created_by=self.request.user)


@require_http_methods(["GET"])
@login_required
def send_email_to_organs(request, pk):
    """
    preparing data and send them to celery task
    """
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
