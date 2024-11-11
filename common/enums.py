from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    INACTIVE = "INACTIVE", _("Inactive")
    DRAFT = "DRAFT", _("Draft")
    RELEASED = "RELEASED", _("Released")
    APPROVED_DRAFT = "APPROVED_DRAFT", _("Approved Draft")
    ABSENT = "ABSENT", _("Absent")
    PURCHASE_ORDER = "PURCHASE_ORDER", _("Purchase Order")
    SUSPEND = "SUSPEND", _("Suspend")
    ON_HOLD = "ON_HOLD", _("On Hold")
    HARDWIRED = "HARDWIRED", _("Hardwired")
    LOSS = "LOSS", _("Loss")
    FREEZE = "FREEZE", _("Freeze")
    FOR_ADJUSTMENT = "FOR_ADJUSTMENT", _("For Adjustment")
    DISTRIBUTOR_ORDER = "DISTRIBUTOR_ORDER", _("Distributor Order")


class UserTypeChoices(models.TextChoices):
    LEAD = "LEAD", _("Lead")
    CLIENT = "CLIENT", _("Client")
    INTRODUCER = "INTRODUCER", _("Introducer")
    SERVICE_HOLDER = "SERVICE_HOLDER", _("Service Holder")


class GenderChoices(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")
    OTHER = "OTHER", _("Other")


class RoleChoices(models.TextChoices):
    INTRODUCER = "INTRODUCER", _("Introducer")
    ADVISOR = "ADVISOR", _("Advisor")
    ADMIN = "ADMIN", _("Admin")
