# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
import base64
import hashlib
from .forms import PaymentForm
from .models import WMTransaction
from django.conf import settings
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from .signals import payment_done

@login_required
def request_payment(request):
    try:
        amount = float(request.POST.get('amount', 0))
    except:
        return HttpResponseBadRequest('Wrong parameters')
    desc = request.POST.get('desc', u'Пополнение счета')
    goal = request.POST.get('goal', None)
    user = request.user
    
    transaction = WMTransaction(user=user, amount=amount, desc=desc, goal=goal)
    transaction.save()
    
    form = PaymentForm(initial={
                                'LMI_PAYMENT_AMOUNT': amount,
                                'LMI_PAYMENT_NO': transaction.pk,
                                'LMI_PAYMENT_DESC_BASE64': base64.b64encode(desc.encode('utf-8')),
                                'LMI_RESULT_URL': getattr(settings, 'WM_RESULT_URL', None),
                                'LMI_SUCCESS_URL': getattr(settings, 'WM_SUCCESS_URL', None),
                                'LMI_FAIL_URL': getattr(settings, 'WM_FAIL_URL', None),
                                })
    
    return render_to_response('django_wm/request_form.djhtml', 
                              {'form': form},
                              RequestContext(request))
    
@csrf_exempt
def process_payment(request):
    try:
        prerequest = int(request.REQUEST.get('LMI_PREREQUEST', 0))
        if prerequest == 1:
            # если это предварительное уведомление, отсылаем YES
            return HttpResponse('YES')
    except:
        pass
    
    LMI_PAYEE_PURSE = request.REQUEST.get('LMI_PAYEE_PURSE', '')
    LMI_PAYMENT_AMOUNT = request.REQUEST.get('LMI_PAYMENT_AMOUNT', '')
    LMI_PAYMENT_NO = request.REQUEST.get('LMI_PAYMENT_NO', '')
    LMI_MODE = request.REQUEST.get('LMI_MODE', '')
    LMI_SYS_INVS_NO = request.REQUEST.get('LMI_SYS_INVS_NO', '')
    LMI_SYS_TRANS_NO = request.REQUEST.get('LMI_SYS_TRANS_NO', '')
    LMI_SYS_TRANS_DATE = request.REQUEST.get('LMI_SYS_TRANS_DATE', '')
    LMI_PAYER_PURSE = request.REQUEST.get('LMI_PAYER_PURSE', '')
    LMI_PAYER_WM = request.REQUEST.get('LMI_PAYER_WM', '')
    LMI_HASH = request.REQUEST.get('LMI_HASH', '')
    
    secret_key = settings.WM_SECRETKEY
    control_hash = hashlib.md5('%s%s%s%s%s%s%s%s%s%s' % (LMI_PAYEE_PURSE, LMI_PAYMENT_AMOUNT, 
                                                         LMI_PAYMENT_NO, LMI_MODE,
                                                         LMI_SYS_INVS_NO, LMI_SYS_TRANS_NO,
                                                         LMI_SYS_TRANS_DATE, secret_key,
                                                         LMI_PAYER_PURSE,LMI_PAYER_WM)).hexdigest().upper()
    if control_hash != LMI_HASH:
        return HttpResponseBadRequest('Wrong checksum')
    
    # все круто, обрабатываем платеж
    try:
        transaction = WMTransaction.objects.get(pk=int(LMI_PAYMENT_NO))
    except:
        # что-то не так, платеж не был найден
        return HttpResponseBadRequest('Wrong LMI_PAYMENT_NO')
        
    if LMI_MODE == '0' or getattr(settings, 'WM_TESTMODE', None):
        transaction.status = 'completed'
        transaction.purse = LMI_PAYER_PURSE
        transaction.save()
        payment_done.send(transaction)
    else:
        return HttpResponseBadRequest('Payment was in TEST MODE')
    
    return HttpResponse('OK')
    
    
        
        
        
    