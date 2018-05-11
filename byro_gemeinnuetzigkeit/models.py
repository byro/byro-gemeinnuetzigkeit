from django.db import models
from django.utils.translation import ugettext_lazy as _

from byro.common.models.configuration import ByroConfiguration

DOCUMENT_CATEGORY = 'zuwendungsbestaetigung'


class GemeinnuetzigkeitConfiguration(ByroConfiguration):

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
        max_length=250,
        verbose_name='Förderungszwecke, Genitiv ("zur Förderung …"), z.B. "der Bildung, sowie der Anarchie"',
    )
    notification_date = models.CharField(
        null=True, blank=True,
        max_length=50,
        verbose_name=_('last date of notification'),
    )
    veranlagungszeitraum = models.CharField(
        null=True, blank=True,
        max_length=50,
        verbose_name=_('Veranlagungszeitraum, z.B. 2016'),
    )
    location = models.CharField(
        null=True, blank=True,
        max_length=50,
        verbose_name=_('Unterschriftsort'),
    )
    receipt_template = models.ForeignKey(
        to='mails.MailTemplate',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
