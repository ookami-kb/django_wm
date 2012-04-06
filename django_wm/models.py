# -*- coding: utf-8 -*
from django.db import models
from django.contrib.auth.models import User
import datetime

class WMTransaction(models.Model):
    STATUSES = (
                ('processing', u'обрабатывается'),
                ('completed', u'завершен'),
                )
    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    status = models.CharField(u'Статус', choices=STATUSES, max_length=15, default='processing')
    created = models.DateTimeField(u'Создан', auto_now_add=True)
    completed = models.DateTimeField(u'Оплачен', required=False)
    amount = models.FloatField(u'Сумма платежа')
    purse = models.CharField(u'Кошелек', max_length=15, required=False)
    
    def save(self, *args, **kwargs):
        if self.status == 'completed':
            self.completed = datetime.datetime.now()
        super(WMTransaction, self).save(*args, **kwargs)