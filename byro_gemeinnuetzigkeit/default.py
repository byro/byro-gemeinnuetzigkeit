from django.utils.translation import ugettext_lazy as _
from i18nfield.strings import LazyI18nString

SUBJECT = LazyI18nString.from_gettext(_('Your Receipt'))
TEXT = LazyI18nString.from_gettext(_('''Hi,

This is your official receipt for fees and donations rendered to us last
year.  As the finance autorities usually do not want to see receipts,
and we are not allowed to sign receipts digitally, please keep it like
this. If you need to send it in, come around and we'll sign it.

Thanks,
the robo clerk'''))
