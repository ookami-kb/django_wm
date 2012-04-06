# -*- coding: utf-8 -*
from django import forms
from django.conf import settings

class PaymentForm(forms.Form):
    LMI_PAYEE_PURSE = forms.CharField(required=False, max_length=15, initial=settings.WM_PURSE, widget=forms.HiddenInput())
    LMI_PAYMENT_AMOUNT = forms.FloatField(min_value=0, widget=forms.HiddenInput())
    LMI_PAYMENT_NO = forms.IntegerField(widget=forms.HiddenInput())
    LMI_PAYMENT_DESC_BASE64 = forms.CharField(widget=forms.HiddenInput())
    LMI_SIM_MODE = forms.IntegerField(initial=0, widget=forms.HiddenInput())
    LMI_RESULT_URL = forms.CharField(required=False, widget=forms.HiddenInput())
    LMI_SUCCESS_URL = forms.CharField(required=False, widget=forms.HiddenInput())
    LMI_FAIL_URL = forms.CharField(required=False, widget=forms.HiddenInput())
    
    