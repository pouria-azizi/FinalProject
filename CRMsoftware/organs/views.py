import logging
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from . import models

logger = logging.getLogger(__name__)  # logger object


@method_decorator(csrf_exempt, name='dispatch')
class CreateNewOrganization(LoginRequiredMixin, CreateView):
    """
    view for create new organization
    """
    form_class = forms.EntryOrganizationForm
    template_name = 'organs/add_entry.html'
    extra_context = {'organization_products': models.OrganizationProduct.objects.all()}

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid input.')
        return reverse_lazy('create_organ')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        try:
            messages.success(self.request, 'Organization created successfully.')
            return super().form_valid(form)
        except:
            messages.error(self.request, 'Invalid input.')
            return redirect(reverse_lazy('create_organ'))

    def get_success_url(self):
        return reverse('organ_list')


@method_decorator(csrf_exempt, name='dispatch')
class EditOrgan(LoginRequiredMixin, UpdateView):
    """
        view for edit organs
    """
    model = models.Organization
    fields = (
        'organization_phone',
        'employees_number',
        'owner',
        'email',
        'owner_phone',
    )
    template_name = 'organs/organization_form.html'
    success_url = reverse_lazy('organ_list')


class OrgansList(ListView):
    """
    Show the list of organs
    """
    model = models.Organization
    template_name = 'organs/organization_list.html'


class OrgansDetail(DetailView):
    """
    Show the detail of organs
    """
    model = models.Organization


class OrganizationNewProduct(CreateView):
    """
    Create new organs product
    """
    model = models.OrganizationProduct
    fields = [
        'name'
    ]
    success_url = reverse_lazy('create_organ')
