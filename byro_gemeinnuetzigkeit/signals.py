from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from byro.office.signals import member_view


@receiver(member_view)
def gemeinnuetzigkeit_member_view(sender, signal, **kwargs):
    member = sender
    return {
        "label": _("Bescheinigung"),
        "url": reverse(
            "plugins:byro_gemeinnuetzigkeit:members.bescheinigung",
            kwargs={"pk": member.pk},
        ),
        "url_name": "plugins:byro_gemeinnuetzigkeit",
    }
