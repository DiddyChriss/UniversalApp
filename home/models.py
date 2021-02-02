from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField
from upload_validator import FileTypeValidator

def validate_phone_number(value):
    if value is not int and '+' is not value[0]:
        raise ValidationError(
            _('Numer telefonu skłąda się wyłącznie z cyfr, poprzedzonych znakiem "+" jako numeru kierunkowego Państwa.'
              ' (np. +48 999999999!)'),
            params={'value': value},
        )

def validate_logo(value):
    validator = FileTypeValidator(allowed_types=['image/*'], allowed_extensions=['.jpg', '.jpeg', '.png'],)
    validator(value)

def validate_pdf(value):
    validator = FileTypeValidator(allowed_types=['application/pdf'],allowed_extensions=['.pdf'])
    validator(value)

class OwnerPanelShop(models.Model):
    company_name = models.CharField(max_length=50, null=True)
    street = models.CharField(max_length=20, null=True)
    street_number = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=20, null=True)
    zipcode = models.CharField(max_length=10, null=True)
    state = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=50, null=True)
    phone_number = models.CharField(max_length=15,
                                    null=True,
                                    blank=True,
                                    validators=[validate_phone_number]
                                    )
    logo = models.FileField(upload_to='owner_panel/', null=True, validators=[validate_logo])
    regulations_pdf = models.FileField(upload_to='owner_panel/', null=True, validators=[validate_pdf])
    privacy_policy_pdf = models.FileField(upload_to='owner_panel/', null=True, validators=[validate_pdf])

    home_title = models.CharField(max_length=15, null=True)
    home_title_2 = models.CharField(max_length=15, null=True)
    home_dics = models.TextField(max_length=60, null=True)
    home_background_img = models.FileField(upload_to='owner_panel/home/', null=True, validators=[validate_logo])
    home_img_1 = models.FileField(upload_to='owner_panel/home/', null=True, validators=[validate_logo])
    home_img_2 = models.FileField(upload_to='owner_panel/home/', null=True, validators=[validate_logo])
    home_img_3 = models.FileField(upload_to='owner_panel/home/', null=True, validators=[validate_logo])

    about_title = models.CharField(max_length=15, null=True)
    about_subtitle = models.CharField(max_length=20, null=True)
    about_textarea_1 = models.TextField(null=True)
    about_img_title_1 = models.CharField(max_length=20, null=True)
    about_textarea_2 = models.TextField(null=True)
    about_img_title_2 = models.CharField(max_length=20, null=True)
    about_textarea_3 = models.TextField(null=True)
    about_img_1 = models.FileField(upload_to='owner_panel/about/', null=True, validators=[validate_logo])
    about_img_2 = models.FileField(upload_to='owner_panel/about/', null=True, validators=[validate_logo])


    class Meta:
        verbose_name_plural = "1. Info-Firma"

    def __str__(self, *args, **kwargs):
            return str(self.company_name)

    def get_logo(self):
        try:
            url = self.logo.url
        except:
            url = ''
        return url

    def get_regulatins_pdf(self):
        try:
            url = self.regulations_pdf.url
        except:
            url = ''
        return url

    def get_privacy_policy_pdf(self):
        try:
            url = self.privacy_policy_pdf.url
        except:
            url = ''
        return url

class ContactModels(models.Model):                  #creating of data in models
    name = models.CharField(max_length=200)
    surname = models.CharField(blank=True, max_length=200)
    company = models.CharField(blank=True, max_length=200)
    date = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=200)
    question = models.TextField()
    confirmation = models.BooleanField(null=True)

    class Meta:
        verbose_name_plural = "2. Formularz Kontaktowy"

    def __str__(self, *args, **kwargs):
        return (self.name)


class Colors(models.Model):
    eshop_background = ColorField(default='#EEEEEE')
    eshop_navbar = ColorField(default='#0047FF')
    eshop_font_nav = ColorField(default='#E6DCE1')
    eshop_container_products = ColorField(default='#C7C7C7')
    eshop_container_products_elemnts = ColorField(default='#EEEEEE')
    eshop_navbar_left = ColorField(default='#BBEDEE')
    eshop_font_nav_left = ColorField(default='#0047FF')
    eshop_font_container = ColorField(default='#1594BC')
    CLASES = [
        ('primary', 'blue'),
        ('secondary', 'gray'),
        ('success', 'green'),
        ('danger', 'red'),
        ('warning', 'yellow'),
        ('info', 'lightblue'),
        ('dark', 'black'),
        ('light', 'light'),
        ]
    eshop_buttons_nav = models.CharField(max_length=10, choices=CLASES, default='blue')
    eshop_buttons_font_nav = models.CharField(max_length=10, choices=CLASES, default='light')

    eshop_buttons_cont = models.CharField(max_length=10, choices=CLASES, default='blue')
    eshop_buttons_font_cont = models.CharField(max_length=10, choices=CLASES, default='light')

    home_font = ColorField(default='#030303')
    home_font_link = ColorField(default='#0A0A0A')
    home_background_eshop = ColorField(default='#ACACAC')
    home_background_eshop_font = ColorField(default='#272526')

    about_background_con = ColorField(default='#ECECEC')
    about_backgound_con_font = ColorField(default='#0A0A0A')

    class Meta:
        verbose_name_plural = "3. Kolory"

    def __str__(self, *args, **kwargs):
        return 'Kolory'
