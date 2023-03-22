from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PluginApp(AppConfig):
    name = "byro_gemeinnuetzigkeit"
    verbose_name = "byro-Plugin für gemeinnützige Vereine"

    class ByroPluginMeta:
        name = ugettext_lazy("byro-Plugin für gemeinnützige Vereine")
        author = "rixx"
        description = ugettext_lazy(
            "byro-Plugin für alle Bedürfnisse des gemeinnützigen Vereins (Spendenbescheinigungen für Mitglieder)"
        )
        visible = True
        version = "0.0.0"

        document_categories = {
            "byro_gemeinnuetzigkeit.receipt": ugettext_lazy(
                "Donation/Membership receipt"
            ),
        }

    def ready(self):
        from . import signals  # NOQA


default_app_config = "byro_gemeinnuetzigkeit.PluginApp"
