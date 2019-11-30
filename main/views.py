import logging
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)

from main.forms import UserCreationForm, ContactForm
from main.models import Product, ProductTag, Address


class ContactUsView(FormView):
    template_name = 'contact_form.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class ProductListView(ListView):
    template_name = 'main/product_list.html'
    paginate_by = 4

    def get_queryset(self):
        # When an instance of this view is created,
        # the attributes args and kwargs are populated
        # with information from the URL route
        tag = self.kwargs['tag']
        self.tag = None
        if tag != 'all':
            self.tag = get_object_or_404(
                ProductTag, slug=tag,
            )
        if self.tag:
            products = Product.objects.active().filter(
                tags=self.tag
            )
        else:
            products = Product.objects.active()

        return products.order_by('name')


logger = logging.getLogger(__name__)


class SignupView(FormView):
    template_name = 'signup.html'
    form_class = UserCreationForm

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        # validate and save the user instance
        response = super().form_valid(form)
        form.save()

        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        logger.info(
            'New signup for email=%s through SignupView', email
        )
        # ensure that the credentials passed are valid according
        # to the authentication backend
        user = authenticate(email=email, password=raw_password)
        # associate the current user and future requests
        # via a session
        login(self.request, user)

        form.send_mail()
        # django message framework used to display flash messages
        # to users, just a form of feedback
        messages.info(
            self.request, 'Signup was successful'
        )

        return response


class AddressListView(LoginRequiredMixin, ListView):
    model = Address

    # the data to populate the view, view has access
    # to the request self.request
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    fields = [
        'name',
        'address1',
        'address2',
        'zip_code',
        'city',
        'country',
    ]

    success_url = reverse_lazy('address_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    fields = [
        'name',
        'address1',
        'address2',
        'zip_code',
        'city',
        'country',
    ]

    success_url = reverse_lazy('address_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    success_url = reverse_lazy('address_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
