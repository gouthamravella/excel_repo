from django.db import models
from django_mysql import models as dmysql
# Create your models here.

class Expressions(models.Model):
    domain = models.CharField('domain', max_length=15, null=True)
    expression = models.TextField('expression', default='', blank=True, null=True)
    intents = dmysql.JSONField('intents', default=list, blank=True, null=True)
    cumulative_cause_intents = dmysql.JSONField('cumulative cause intents', default=list, blank=True, null=True)
    cumulative_effect_intents = dmysql.JSONField('cumulative effect intents', default=list, blank=True, null=True)
    datecreated = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['domain',]),
        ]

    def __str__(self):
        return self.id
    