import logging
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from . import models
from products.models import Product # noqa

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

    def get_success_url(self):
        return reverse('organ_list')


class OrgansList(ListView):
    """
    Show the list of organs
    """
    model = models.Organization
    template_name = 'organs/organization_list.html'
    paginate_by = 5

    # def get_queryset(self):
    #     return models.Organization.objects.filter(created_by=self.request.user)


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


class OrganizationNewProduct(CreateView):
    """
    Create new organs product
    """
    model = models.OrganizationProduct
    fields = [
        'name'
    ]
    success_url = reverse_lazy('create_organ')
