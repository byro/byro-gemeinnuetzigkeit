from decimal import Decimal
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from num2words import num2words as lib_num2words
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from byro.common.models import Configuration
from byro.documents.models import Document

from .models import DOCUMENT_CATEGORY, GemeinnuetzigkeitConfiguration
from .pdf import CURRENCY, FONTSIZE, get_default_document, get_paragraph_style


def generate_donation_receipt(member, year):
    fees = member.fee_payments.filter(value_datetime__year=year).aggregate(fees=models.Sum('amount'))['fees'] or Decimal('0.00')
    donations = member.donations.filter(value_datetime__year=year).aggregate(donations=models.Sum('amount'))['donations'] or Decimal('0.00')
    address = member.address
    if (donations + fees) <= 0:
        raise Exception('No donations or fees for {year}.'.format(year=year))

    story = []
    _buffer = BytesIO()
    local_settings = GemeinnuetzigkeitConfiguration.get_solo()
    global_settings = Configuration.get_solo()
    doc = get_default_document(_buffer)
    style = get_paragraph_style()

    # Header
    our_address = '\n'.join([global_settings.name, global_settings.address]).replace('\n', '<br />')
    our_address = Paragraph(our_address, style['Normal'])
    our_title = Paragraph('Aussteller (Steuerbegünstigte Einrichtung)', style['Heading5'])
    story.append(Table(
        [[our_title, ], [our_address, ]],
        colWidths=[doc.width * 1],
        hAlign='LEFT',
        style=TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('BOX', (0, 0), (0, 1), 0.5, colors.black),
        ]),
    ))
    story.append(Paragraph('Bestätigung über Geldzuwendungen/Mitgliedsbeitrag', style['Heading3']))
    story.append(Paragraph('im Sinne des § 10b des Einkommenssteuergesetzes an eine der in § 5 Abs. 1 Nr. 9 des Körperschaftssteuergesetzes bezeichneten Körperschaften, Personenvereinigungen oder Vermögensmassen', style['Normal']))
    story.append(Spacer(1, 5 * mm))

    their_address = address.replace('\n', '<br />')
    their_address = Paragraph(their_address, style['Normal'])
    their_title = Paragraph('Name und Anschrift des Zuwendenden', style['Heading5'])
    story.append(Table(
        [[their_title], [their_address]],
        colWidths=[doc.width * 1],
        style=TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('BOX', (0, 0), (0, 1), 0.5, colors.black),
        ]),
    ))
    story.append(Spacer(1, 5 * mm))

    data = [[_('Product'), _('Tax rate'), _('Net'), _('Gross')], ]
    data = [['Art', 'in Ziffern', 'in Buchstaben', 'Datum']]
    if fees:
        data.append(['Beiträge', CURRENCY.format(fees), lib_num2words(fees, lang='de'), year])
    if donations:
        data.append(['Spenden', CURRENCY.format(donations), lib_num2words(donations, lang='de'), year])
    last_row = len(data) - 1

    story.append(Table(
        data=data,
        colWidths=[doc.width*0.15, doc.width*0.15, doc.width*0.5, doc.width*0.2],
        style=TableStyle([
            ('FONTSIZE', (0, 0), (3, last_row), FONTSIZE),
            ('ALIGN', (0, 0), (1, last_row), 'LEFT'),
            ('ALIGN', (3, 0), (3, last_row), 'RIGHT'),
            ('BOX', (0, 0), (3, last_row), 1.0, colors.black),
            ('GRID', (0, 0), (3, last_row), 0.5, colors.black),
        ]),
    ))
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph('Es handelt sich NICHT um den Verzicht auf Erstattung von Aufwendungen.', style['Normal']))
    story.append(Spacer(1, 5 * mm))
    loong = 'Wir sind wegen Förderung {zwecke} nach dem Freistellungsbescheid bzw. nach der Anlage zum Körperschaftssteuerbescheid des Finanzamts {amt} StNr. {nummer} vom {datum} für den letzten Veranlagungszeitraum {zeitraum} nach § 5 Abs. 1 Nr. 9 des Körperschaftssteuergesetzes von der Körperschaftssteuer und nach § 3 Nr. 6 des Gewerbesteuergesetzes von der Gewerbesteuer befreit.'
    loong = loong.format(
        zwecke=local_settings.reason,
        amt=local_settings.finanzamt,
        nummer=local_settings.vat_id,
        datum=local_settings.notification_date,
        zeitraum=local_settings.veranlagungszeitraum,
    )
    story.append(Paragraph(loong, style['Normal']))
    story.append(Spacer(1, 5 * mm))
    story.append(Table(
        [[Paragraph('Es wird bestätigt, dass die Zuwendung nur zur Förderung {zwecke} verwendet wird.'.format(zwecke=local_settings.reason), style['Normal'])]],
        colWidths=[doc.width * 1],
        style=TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('BOX', (0, 0), (0, 0), 0.5, colors.black),
        ]),
    ))

    story.append(Spacer(1, 25 * mm))
    data = [['{location}, {date}'.format(location=local_settings.location, date=now().date().isoformat())], ['(Ort, Datum, und Unterschrift des Zuwendungsempfängers)']]
    story.append(Table(
        data=data,
        colWidths=[doc.width],
        style=TableStyle([
            ('LINEABOVE', (0, 1), (0, 1), 1.0, colors.black),
        ]),
    ))

    story.append(Spacer(1, 5 * mm))
    disclaimer1 = 'Wer vorsätzlich oder grob fahrlässig eine unrichtige Zuwendungsbestätigung erstellt oder wer veranlasst, dass Zuwendungen nicht zu den in der Zuwendungsbestätigung angegebenen steuerbegünstigten Zwecken verwendet werden, haftet für die Steuer, die dem Fiskus durch einen etwaigen Abzug der Zuwendungen beim Zuwendenden entgeht (§10b Abs. 4 EStG, §9 Abs. 3 KStG, §9 Nr. 5 GewStG).'
    disclaimer2 = 'Diese Bestätigung wird nicht als Nachweis für die steuerliche Berücksichtigung der Zuwendung anerkannt, wenn das Datum des Freistellungsbescheides länger als 5 Jahre bzw. das Datum der vorläufigen Bescheinigung länger als 3 Jahre seit Ausstellung der Bestätigung zurückliegt (BMF vom 15.12.1994 – BStBl I S. 884).'
    story.append(Paragraph('Hinweis', style['Heading5']))
    story.append(Paragraph(disclaimer1, style['Normal']))
    story.append(Paragraph(disclaimer2, style['Normal']))

    doc.build(story)
    _buffer.seek(0)
    doc = Document.objects.create(
        title='Zuwendungsbestätigung {}'.format(year),
        category=DOCUMENT_CATEGORY,
        member=member,
    )
    doc.document.save('spenden/spenden_{}_{}_{}.pdf'.format(year, member.number, member.name), ContentFile(_buffer.read()))
    doc.save()
    return doc.document.url
