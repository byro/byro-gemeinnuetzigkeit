from django.conf.global_settings import LANGUAGES
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel


DOCUMENT_CATEGORY = 'zuwendungsbestaetigung'


class GemeinnuetzigkeitConfiguration(SingletonModel):

    finanzamt = models.CharField(
        null=True, blank=True,
        max_length=300,
        verbose_name=_('Finanzamt'),
    )
    vat_id = models.CharField(
        null=True, blank=True,
        max_length=50,
        verbose_name=_('VAT-ID'),
    )
    reason = models.CharField(
        null=True, blank=True,
        max_length=50,
        verbose_name=_('reason for reduced taxes'),
    )
    notification_date = models.CharField(
        null=True, blank=True,
        max_length=50,
        verbose_name=_('last date of notification'),
    )
