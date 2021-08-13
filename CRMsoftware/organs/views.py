import logging
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from . import models, serializers, forms
from products.models import Product  # noqa
from rest_framework import generics, filters, viewsets, permissions
from rest_framework.exceptions import NotAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)  # logger object


@method_decorator(csrf_exempt, name='dispatch')
class CreateNewOrganization(LoginRequiredMixin, CreateView):
    """
    view for create new organization
    """
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
    ]
    template_name = 'organs/add_entry.html'
    extra_context = {'organization_products': models.OrganizationProduct.objects.all()}

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid input.')
        return reverse_lazy('create_organ')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        try:
            messages.success(self.request, 'سازمان جدید به لیست سازمانها اضافه شد')
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

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid input.')
        return reverse_lazy('create_organ')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        try:
            messages.success(self.request, 'مشخصات سازمان با موفقیت ویرایش شد')
            return super().form_valid(form)
        except:
            messages.error(self.request, 'Invalid input.')
            return redirect(reverse_lazy('create_organ'))

    def get_queryset(self):
        return models.Organization.objects.filter(created_by=self.request.user)

    def get_success_url(self):
        return reverse('organ_list')


class OrgansList(LoginRequiredMixin, ListView):
    """
    Show the list of organs
    """
    model = models.Organization
    template_name = 'organs/organization_list.html'
    paginate_by = 5

    def get_queryset(self):
        return models.Organization.objects.filter(created_by=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
class OrgansDetail(LoginRequiredMixin, DetailView):
    """
    Show the detail of organs
    """
    model = models.Organization

    def get_related_products(self):
        organ = self.get_object()
        organ_products = organ.organization_product.all()
        related = Product.objects.filter(follow_product__in=organ_products).distinct()
        return related

    def get_context_data(self, **kwargs):
        c = super().get_context_data()
        c['offer_product'] = self.get_related_products()
        return c

    def get_queryset(self):
        return models.Organization.objects.filter(created_by=self.request.user)


class OrganizationNewProduct(LoginRequiredMixin, CreateView):
    """
    Create new organs product
    """
    model = models.OrganizationProduct
    fields = [
        'name'
    ]
    success_url = reverse_lazy('create_organ')


@method_decorator(csrf_exempt, name='dispatch')
class CreateFollowUp(LoginRequiredMixin, CreateView):
    """
    Create new followUp for organs
    """
    model = models.FollowUp
    fields = [
        'description'
    ]
    template_name = 'organs/followup_form.html'

    def form_invalid(self, form):
        return JsonResponse(data={
            'success': 'False',
        }, status=400)

    def form_valid(self, form):
        form.save(commit=False).created_by = self.request.user
        form.save(commit=False).organ = models.Organization.objects.get(pk=self.kwargs['pk'])
        form.save()
        return JsonResponse(data={
            'success': 'True',
        }, status=200)

    def get_context_data(self, **kwargs):
        context = {
            'organ_obj': models.Organization.objects.get(pk=self.kwargs['pk']),
        }
        return context


class FollowUpDetail(LoginRequiredMixin, DetailView):
    queryset = models.FollowUp.objects.all()
    template_name = 'organs/followup_detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(FollowUpDetail, self).get_context_data(**kwargs)
        context['description'] = models.FollowUp.objects.filter(organ_id=pk)
        return context

    def get_queryset(self):
        return models.Organization.objects.filter(created_by=self.request.user)


"""
DRF
"""


class OrgansListApi(viewsets.ModelViewSet):
    """
    this view can represent api for organizations data
    """
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrgansSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]

    # token = Token.objects.create(user=models.Organization.created_by)
    # print(token.key)

    def get_queryset(self):
        return models.Organization.objects.filter(created_by_id=self.request.user.pk)
