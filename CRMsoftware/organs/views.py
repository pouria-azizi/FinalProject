import logging

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from . import models

logger = logging.getLogger(__name__)  # logger object


@method_decorator(csrf_exempt, name='dispatch')
class CreateNewOrganization(LoginRequiredMixin, CreateView):

    queryset = models.Organization.objects.all()
    fields = [
        'province',
        'name',
        'organization_phone',
        'employees_number',
        'owner',
        'email',
        'owner_phone',
        'organization_product',
        'created_by'
    ]
    template_name = 'organs/add_entry.html'
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        qs = models.Organization.save.user = self.request.user
        return qs


@method_decorator(csrf_exempt, name='dispatch')
class EditOrgan(LoginRequiredMixin, UpdateView):
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
    model = models.Organization
    template_name = 'organs/organization_list.html'


class OrgansDetail(DetailView):
    model = models.Organization


class OrganizationNewProduct(CreateView):
    model = models.OrganizationProduct
    fields = [
        'name'
    ]
    success_url = reverse_lazy('create_organ')
    # def get_queryset(self):
    #     organ_p = forms.EntryOrganizationForm.
    #     return organ_p


# @method_decorator(c/srf_exempt, name='dispatch')
# class ShowAddEntryForm(CreateView):
#     """
#     Show the add entry form page
#     """
#     model = models.OrganizationProduct
#     fields = [
#         'name'
#     ]
#     template_name = 'organs/product_entry.html'
#     success_url = reverse_lazy('organ_product')
