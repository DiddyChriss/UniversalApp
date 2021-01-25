from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.template import loader
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View

from .forms import *
from eshop.forms import *
from .models import *
from eshop.models import *
from eshop.views import *



def base_view(request):
    template_name = 'home/base_home.html'
    return render(request, template_name, {})

class ContactView(ShopGetView, View):
    template_name = 'home/contact.html'

    def post(self, request, pk=None, *args, **kwargs):
        contact_form = ContactForms(self.request.POST or None)
        form = SearchForm(self.request.POST or None)
        owner_panel_shop = OwnerPanelShop.objects.all().first()
        colors = Colors.objects.all().first()
        queryset_cart_all_users = OrderItem.objects.all()
        category = Category.objects.all()
        queryset = ''
        try:
            if request.user.is_authenticated:
                customer = Customer.objects.get(user=request.user)
            else:
                device = request.COOKIES['device']
                customer, created = Customer.objects.get_or_create(device=device)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            queryset_cart = []
            for user_item in queryset_cart_all_users:
                if user_item.order == order:
                    queryset_cart.append(user_item)
        except:
            queryset_cart = []
        if 'search' in self.request.POST and form.is_bound and form.is_valid():  # use seerch
            form_value = form.cleaned_data['search_product']
            queryset = Product.objects.filter(title_product__icontains=form_value)
            messages.info(request, 'Znalezione produkty:', extra_tags="info")
        elif 'contact' in self.request.POST and contact_form.is_valid():
            confirmation = contact_form.cleaned_data.get('confirmation')
            email = contact_form.cleaned_data.get('email')
            name = contact_form.cleaned_data.get('name')
            surname = contact_form.cleaned_data.get('surname')
            question = contact_form.cleaned_data.get('question')
            contact_form.save()

            if confirmation == True:
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

            messages.info(request,
                          'Dziękujemy {} {} za skorzystanie z Formularza Kontaktowego! Kopia formularza'
                          ' została wysłana na adres e-mail: {}'.format(name.capitalize(),
                                                                        surname.capitalize(),
                                                                        email,
                                                                        ),
                                                                        extra_tags="info")
            return redirect('/kontakt/')


        form = SearchForm()
        contact_form = ContactForms()
        context = {
            'contact_form': contact_form,
            'form': form,
            'owner_panel_shop': owner_panel_shop,
            'colors': colors,
            'shop_products': queryset,
            'shop_products_cart': len(queryset_cart),
            'category': category,
        }
        return render(self.request, 'shop/shop_search.html', context)