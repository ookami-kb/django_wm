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
    completed = models.DateTimeField(u'Оплачен', null=True, blank=True)
    amount = models.FloatField(u'Сумма платежа')
    purse = models.CharField(u'Кошелек', max_length=15, null=True, blank=True)
    desc = models.CharField(u'Описание', max_length=255, null=True, blank=True)
    goal = models.CharField(u'Назначение', max_length=30, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.status == 'completed':
            self.completed = datetime.datetime.now()
        super(WMTransaction, self).save(*args, **kwargs)