from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView

from main.views import ContactUsView, ProductListView, SignupView
from main.models import Product
from main.forms import AuthenticationForm

urlpatterns = [
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('about-us/', TemplateView.as_view(template_name='about_us.html',
                                           ), name='about_us'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path(
        'products/<slug:tag>/',
        ProductListView.as_view(),
        name='products',
    ),
    path(
        'product/<slug:slug>/',
        DetailView.as_view(model=Product),
        name='product',
    ),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(
        template_name='login.html',
        form_class=AuthenticationForm,
    ),
     name='login')
]
