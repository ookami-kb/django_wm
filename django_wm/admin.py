from django.contrib import admin
from .models import WMTransaction

class WMTransactionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'created', 'status', 'completed', 'amount', 'purse')
admin.site.register(WMTransaction, WMTransactionAdmin)