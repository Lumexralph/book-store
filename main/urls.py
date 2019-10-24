from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from main import views
from main.models import Product

urlpatterns = [
    path('contact-us/', views.ContactUsView.as_view(), name='contact-us'),
    path('about-us/', TemplateView.as_view(template_name='about_us.html',
                                           ), name='about_us'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path(
        'products/<slug:tag>/',
        views.ProductListView.as_view(),
        name='products',
    ),
    path(
        'product/<slug:slug>',
        DetailView.as_view(model=Product),
        name='product',
    ),
]
