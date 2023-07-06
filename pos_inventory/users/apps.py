from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "pos_inventory.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import pos_inventory.users.signals  # noqa: F401
        except ImportError:
            pass
