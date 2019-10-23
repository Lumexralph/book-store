from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from main import forms
from main.models import Product, ProductImage, ProductTag


class ContactUsView(FormView):
    template_name = 'contact_form.html'
    form_class = forms.ContactForm
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
