from django import forms
from django.utils.timezone import now
from django.shortcuts import redirect
from django.views.generic import FormView

from byro.office.views.members import MemberView

from .donations import generate_donation_receipt
from .models import DOCUMENT_CATEGORY


class YearForm(forms.Form):
    year = forms.ChoiceField()

    def __init__(self, *args, member=None, **kwargs):
        super().__init__(*args, **kwargs)
        min_year = member.transactions.all().order_by('value_datetime').first()
        max_year = member.transactions.all().order_by('-value_datetime').first()
        if min_year:
            current_year = now().year
            years = range(min_year.value_datetime.year, max_year.value_datetime.year + 1)
            self.fields['year'].choices = ((y, y) for y in years if y < current_year)


class Bescheinigung(MemberView, FormView):
    form_class = YearForm
    template_name = 'byro_gemeinnuetzigkeit/bescheinigung.html'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['member'] = self.get_object()
        return kwargs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['receipts'] = self.get_object().documents.filter(category=DOCUMENT_CATEGORY)
        return ctx

    def post(self, request, pk):
        self.object = self.get_object()
        form = YearForm(self.request.POST, member=self.object)
        if form.is_valid():
            year = form.cleaned_data['year']
            old_documents = self.object.documents.filter(category=DOCUMENT_CATEGORY, title__endswith=year)
            old = len(old_documents)
            document = generate_donation_receipt(self.object, year)
            if old:
                old_documents.delete()
        return redirect(self.request.path)


class SendBescheinigung(FormView):
    pass
