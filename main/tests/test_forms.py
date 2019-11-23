from django.test import TestCase
from django.core import mail
from django.urls import reverse

from main.forms import ContactForm, UserCreationForm


class TestForm(TestCase):
    def test_valid_contact_us_forms_sends_email(self):
        form = ContactForm({
            'name': 'Olumide Ogundele',
            'message': 'Hello There',
        })

        self.assertTrue(form.is_valid())

        # using a context manager to send the mail
        with self.assertLogs('main.forms', level='INFO') as cm:
            form.send_mail()

            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].subject, 'Site message')
            self.assertGreaterEqual(len(cm.output), 1)

    def test_invalid_contact_us_form(self):
        form = ContactForm({
            'message': 'Hi Nikky',
        })

        self.assertFalse(form.is_valid())

    def test_contact_us_page_works(self):
        response = self.client.get(reverse('contact-us'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('main/contact_form.html')
        self.assertContains(response, 'BookStore')
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_valid_signup_form_sends_email(self):
        form = UserCreationForm({
            'email': 'user@domain.com',
            'password1': 'abcabcabc',
            'password2': 'abcabcabc',
        })

        self.assertTrue(form.is_valid())

        with self.assertLogs("main.forms", level='INFO') as cm:
            form.send_mail()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Welcome to BookStore')
        self.assertGreaterEqual(len(cm.output), 1)
