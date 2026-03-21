from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PluginApp(AppConfig):
    name = "byro_gemeinnuetzigkeit"
    verbose_name = "byro-Plugin für gemeinnützige Vereine"

    class ByroPluginMeta:
        name = _("byro-Plugin für gemeinnützige Vereine")
        author = "rixx"
        description = _(
            "byro-Plugin für alle Bedürfnisse des gemeinnützigen Vereins (Spendenbescheinigungen für Mitglieder)"
        )
        visible = True
        version = "0.0.0"

        document_categories = {
            "byro_gemeinnuetzigkeit.receipt": _(
                "Donation/Membership receipt"
            ),
        }

    def ready(self):
        from . import signals  # NOQA


default_app_config = "byro_gemeinnuetzigkeit.PluginApp"
