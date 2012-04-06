import django.dispatch

payment_init = django.dispatch.Signal()
payment_done = django.dispatch.Signal()
