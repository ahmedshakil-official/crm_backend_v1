from django.contrib.auth import get_user_model
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_filters.conf import settings

from common.enums import GenderChoices, RoleChoices
from common.fields import TimestampThumbnailImageField
from common.models import NameSlugDescriptionBaseModel, CreatedAtUpdatedAtBaseModel
from authentication.models import User

# User = get_user_model()


class Organization(NameSlugDescriptionBaseModel):
    email = models.EmailField(unique=True)
    logo = TimestampThumbnailImageField(
        upload_to="organization/logo", blank=True, null=True
    )
    profile_image = TimestampThumbnailImageField(
        upload_to="organization/profile", blank=True, null=True
    )
    hero_image = TimestampThumbnailImageField(
        upload_to="organization/hero", blank=True, null=True
    )
    primary_mobile = models.CharField(max_length=20)
    other_contact = models.CharField(max_length=64, blank=True, null=True)
    contact_person = models.CharField(max_length=64, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    contact_person_designation = models.CharField(max_length=64, blank=True, null=True)
    license_no = models.CharField(max_length=128, blank=True, null=True)
    license_image = TimestampThumbnailImageField(
        upload_to="organization/license", blank=True, null=True
    )
    is_removed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class OrganizationUser(CreatedAtUpdatedAtBaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="organization_users",
        verbose_name=_("User"),
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="organization_users",
        verbose_name=_("Organization"),
    )
    role = models.CharField(
        max_length=64,
        choices=RoleChoices.choices,
        default=RoleChoices.ADVISOR,
        verbose_name=_("Role"),
    )
    designation = models.CharField(
        max_length=128, blank=True, null=True, verbose_name=_("Designation")
    )
    official_email = models.EmailField(
        max_length=255, blank=True, null=True, verbose_name=_("Official Email")
    )
    official_phone = models.CharField(
        max_length=24, blank=True, null=True, verbose_name=_("Official Phone")
    )
    permanent_address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Permanent Address")
    )
    present_address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Present Address")
    )
    dob = models.DateField(blank=True, null=True, verbose_name=_("Date of Birth"))
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        default=GenderChoices.MALE,
        verbose_name=_("Gender"),
    )
    joining_date = models.DateField(
        blank=True, null=True, verbose_name=_("Joining Date")
    )
    registration_number = models.CharField(
        max_length=64, blank=True, null=True, verbose_name=_("Registration Number")
    )
    degree = models.CharField(
        max_length=256, blank=True, null=True, verbose_name=_("Degree")
    )

    class Meta:
        unique_together = ("user", "organization")
        verbose_name = _("Organization User")
        verbose_name_plural = _("Organization Users")

    def __str__(self):
        return f"{self.user.email} - {self.organization.name} ({self.role})"
