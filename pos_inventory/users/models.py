from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, UUIDField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import uuid as uuid_lib


class User(AbstractUser):
    """
    Default custom user model for Pos Inventory.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    uuid = UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    first_name = CharField(_("Firts Name of User"), blank=True, max_length=255)  # type: ignore
    last_name = CharField(_("Last Name of User"), blank=True, max_length=255)  # type: ignore

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
