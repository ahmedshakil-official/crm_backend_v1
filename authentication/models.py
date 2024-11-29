from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.enums import UserTypeChoices
from common.fields import TimestampThumbnailImageField
from common.models import CreatedAtUpdatedAtBaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        extra_fields.setdefault("first_name", "")
        extra_fields.setdefault("last_name", "")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("first_name", "")
        extra_fields.setdefault("last_name", "")
        extra_fields.setdefault("phone", "")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, CreatedAtUpdatedAtBaseModel):

    email = models.EmailField(db_index=True, unique=True, null=False, default=None)
    phone = models.CharField(
        db_index=True, max_length=24, unique=False, null=True, blank=True, default=None
    )
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    profile_image = TimestampThumbnailImageField(
        upload_to="user/profile", blank=True, null=True
    )

    nid = models.CharField(
        max_length=64,
        unique=True,
        default=None,
        blank=True,
        null=True,
        verbose_name=_("NID No."),
        help_text=_("National ID No. Example: YYYYXXXXXXXXXXXXX"),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active."),
    )
    user_type = models.CharField(
        max_length=20, choices=UserTypeChoices.choices, default=UserTypeChoices.LEAD
    )
    city = models.CharField(
        db_index=True, max_length=64, unique=False, null=True, blank=True, default=None
    )
    state = models.CharField(
        db_index=True, max_length=64, unique=False, null=True, blank=True, default=None
    )
    country = models.CharField(
        db_index=True, max_length=64, unique=False, null=True, blank=True, default=None
    )
    zip_code = models.CharField(
        db_index=True, max_length=64, unique=False, null=True, blank=True, default=None
    )
    address = models.CharField(
        db_index=True, max_length=255, unique=False, null=True, blank=True, default=None
    )
    groups = models.ManyToManyField(
        "auth.Group", related_name="organization_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="organization_user_permissions", blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
