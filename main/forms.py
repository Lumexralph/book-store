from django import forms
from django.core.mail import send_mail
import logging
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm, UsernameField
)

from main.models import User


logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    message = forms.CharField(max_length=600, widget=forms.Textarea)

    def send_mail(self):
        logger.info('Sending email to customer service')
        message = 'From: {0} \n {1}'.format(
            self.cleaned_data['name'],
            self.cleaned_data['message'],
        )

        send_mail(
            'Site message',
            message,
            'site@bookstore.domain',
            ['customerservice@bookstore.domain'],
            fail_silently=False,
        )


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ('email',)
        field_classes = {'email': UsernameField}

    def send_mail(self):
        logger.info(
            'Sending account registration email to email=%s',
            self.cleaned_data['email'],
        )
        message = 'Welcome {}'.format(self.cleaned_data['email'])
        send_mail(
            'Welcome to BookStore',
            message,
            'site@bookstore.domain'
            [self.cleaned_data['email']],
            fail_silently=True,
        )