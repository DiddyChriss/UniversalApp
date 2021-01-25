from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.template import loader
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View

from .forms import *
from .models import *


def base_view(request):
    template_name = 'home/base_home.html'
    return render(request, template_name, {})

class ContactView(View):
    template_name = 'home/contact.html'
    def get(self,request, pk=None,  *args, **kwargs):
        contact_form = ContactForms()
        owner_panel_shop = OwnerPanelShop.objects.all().first()
        colors = Colors.objects.all().first()
        context = {
            'contact_form': contact_form,
            'colors': colors,
            'owner_panel_shop': owner_panel_shop,
        }
        return render(self.request, self.template_name, context)

    def post(self, request, pk=None, *args, **kwargs):
        contact_form = ContactForms(self.request.POST or None)
        owner_panel_shop = OwnerPanelShop.objects.all().first()
        colors = Colors.objects.all().first()
        if self.request.POST and contact_form.is_valid():
            confirmation = contact_form.cleaned_data.get('confirmation')
            email = contact_form.cleaned_data.get('email')
            name = contact_form.cleaned_data.get('name')
            surname = contact_form.cleaned_data.get('surname')
            question = contact_form.cleaned_data.get('question')
            contact_form.save()

            if confirmation == True:
                send = 'Kopia formularza kontaktowego została wysłana na adres e-mail: {}'.format(email)

                subject = 'Formularz kontaktowy {} - kopia'.format(owner_panel_shop.company_name)    # subject of email

                message = 'Dziękujemy za skorzystanie z Formularza Kontaktowego {}'.format(
                                                              owner_panel_shop.company_name)
                from_email = settings.EMAIL_HOST_USER                     # adres from send and details from settings

                recipient_list = [email, from_email]          # delivery email
                html_message = loader.render_to_string('home/emailsend.html',
                                                       {
                                                        'name': name.capitalize(),
                                                        'surname': surname.capitalize(),
                                                        'question': question,
                                                        'owner_panel_shop': owner_panel_shop,
                                                        }
                                                        )     # render body from html(templates)

                send_mail(subject, message, from_email, recipient_list, fail_silently=True, auth_user=None,
                          auth_password=None, html_message=html_message      # send_mail function
                          )
            else:
                send = ''

            confirmation_text = 'Dziękujemy {} {} za skorzystanie z Formularza Kontaktowego!'.format(
                                                                                                    name.capitalize(),
                                                                                                    surname.capitalize()
                                                                                                    )

        contact_form = ContactForms()
        context = {
            'contact_form': contact_form,
            'owner_panel_shop': owner_panel_shop,
            'colors': colors,
            'send': send,
            'confirmation_text' : confirmation_text,
        }
        return render(self.request, self.template_name, context)


