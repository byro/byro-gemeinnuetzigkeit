from django import forms
from django.views.generic import FormView

from byro.office.views.members import MemberView


class YearForm(forms.Form):
    year = forms.ChoiceField()

    def __init__(self, member, *args, **kwargs):
        super().__init__()
        min_year = member.transactions.all().order_by('value_datetime').first()
        max_year = member.transactions.all().order_by('-value_datetime').first()
        if min_year:
            years = range(min_year, max_year + 1)
            self.fields.year.choices = ((y, y) for y in years)


class Bescheinigung(MemberView, FormView):
    form_class = YearForm
    template_name = 'byro_gemeinnuetzigkeit/bescheinigung.html'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['member'] = self.get_object()
        return kwargs


class SendBescheinigung(FormView):
    pass
