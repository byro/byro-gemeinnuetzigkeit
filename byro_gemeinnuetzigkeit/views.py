from django import forms
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, View

from byro.bookkeeping.models.transaction import Transaction
from byro.office.views.members import MemberView

from .donations import generate_donation_receipt
from .models import DOCUMENT_CATEGORY, GemeinnuetzigkeitConfiguration


class YearForm(forms.Form):
    year = forms.ChoiceField()

    def __init__(self, *args, member=None, **kwargs):
        super().__init__(*args, **kwargs)
        min_year = (
            Transaction.objects.filter(bookings__member=member)
            .order_by("value_datetime")
            .first()
        )
        max_year = (
            Transaction.objects.filter(bookings__member=member)
            .order_by("-value_datetime")
            .first()
        )
        if min_year:
            current_year = now().year
            years = range(
                min_year.value_datetime.year, max_year.value_datetime.year + 1
            )
            self.fields["year"].choices = ((y, y) for y in years if y < current_year)


class Bescheinigung(MemberView, FormView):
    form_class = YearForm
    template_name = "byro_gemeinnuetzigkeit/bescheinigung.html"

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["member"] = self.get_object()
        return kwargs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["receipts"] = self.get_object().documents.filter(category=DOCUMENT_CATEGORY)
        return ctx

    @transaction.atomic
    def post(self, request, pk):
        self.object = self.get_object()
        form = YearForm(self.request.POST, member=self.object)
        if form.is_valid():
            year = form.cleaned_data["year"]
            old_documents = self.object.documents.filter(
                category=DOCUMENT_CATEGORY, title__endswith=year
            )
            old_documents.delete()
            try:
                receipt = generate_donation_receipt(self.object, year)
                self.object.log(
                    self,
                    "byro_gemeinnuetzigkeit.receipt.created",
                    year=year,
                    receipt=receipt,
                )
            except Exception:
                messages.error(
                    request,
                    _("No donations or paid fees for {year}.").format(year=year),
                )
        return redirect(self.request.path)


class SendBescheinigung(MemberView, View):
    def dispatch(self, *args, **kwargs):
        member = self.get_object()
        document = member.documents.get(pk=self.kwargs["receipt"])
        config = GemeinnuetzigkeitConfiguration.get_solo()
        if not config.receipt_template:
            from byro.mails.models import MailTemplate

            from .default import SUBJECT, TEXT

            config.receipt_template = MailTemplate.objects.create(
                subject=SUBJECT, text=TEXT
            )
        config.receipt_template.to_mail(member.email, attachments=[document])
        return redirect(
            reverse(
                "plugins:byro_gemeinnuetzigkeit:members.bescheinigung",
                kwargs={"pk": self.kwargs["pk"]},
            )
        )
