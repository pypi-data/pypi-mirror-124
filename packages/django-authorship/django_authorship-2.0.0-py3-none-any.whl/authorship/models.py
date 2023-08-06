import typing

from django.contrib.auth import models as auth
from django.db import models

from . import settings


class Authorship(models.Model):
    """Abstract model to track when an instance was created/updated and by
    whom."""

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    """:py:class:`datetime` for when this object was first created."""

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        related_name="+",
        on_delete=models.PROTECT,
    )
    """User who first created this object (required)."""

    updated_at = models.DateTimeField(auto_now=True, editable=False)
    """:py:class:`datetime` for when this object was last saved."""

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        related_name="+",
        on_delete=models.PROTECT,
    )
    """User who last saved this object (required)."""

    class Meta:
        abstract = True

    def save(  # type: ignore[override]
        self,
        *,
        user: typing.Optional[auth.AbstractBaseUser] = None,
        **kwargs: typing.Any
    ) -> None:
        """A custom ``Model.save()`` method that appropriately populates
        authorship fields."""
        update_fields = kwargs.pop("update_fields", None)

        if update_fields is not None and "updated_at" not in update_fields:
            update_fields.append("updated_at")

        if user is not None:

            self.updated_by = user  # type: ignore[assignment]
            if update_fields is not None and "updated_by" not in update_fields:
                update_fields.append("updated_by")

            if not self.created_at:
                self.created_by = user  # type: ignore[assignment]

        if update_fields:
            kwargs.update({"update_fields": update_fields})

        return super().save(**kwargs)
