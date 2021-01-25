from django import forms
from .models import *


class ContactForms(forms.ModelForm):
    name = forms.CharField(label='',
                            required=True,
                            widget=forms.TextInput(
                                                    attrs={
                                                            "class": "form-control"
                                                           }
                                                  )
                            )
    surname = forms.CharField(label='',
                               required=False,
                               widget=forms.TextInput(
                                                       attrs={
                                                              "class": "form-control"
                                                              }
                                                      )
                               )
    company = forms.CharField(label='',
                              required=False,
                              widget=forms.TextInput(
                                                     attrs={
                                                            "class": "form-control"
                                                            }
                                                     )
                              )
    email = forms.EmailField(label='',
                              required=True,
                              widget=forms.EmailInput(
                                                      attrs={
                                                             "class": "form-control"
                                                             }
                                                      )
                              )
    question = forms.CharField(label='',
                               required=True,
                               widget=forms.Textarea(
                                                     attrs={
                                                            "rows": 5,
                                                            "cols": 65,
                                                            "class": "form-control"
                                                            }
                                                     )
                               )
    confirmation = forms.BooleanField(initial=True)

    class Meta:
        model = ContactModels
        fields = [
            'name',
            'surname',
            'company',
            'email',
            'question',
            'confirmation',
        ]