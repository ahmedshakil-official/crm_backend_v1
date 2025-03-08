from django.contrib import admin

from case.models import (
    Case,
    Files,
    JointUser,
    ApplicantDetails,
    CompanyInfo,
    Dependant,
    DirectorShareholder,
    Adverse,
Property
)

# Register your models here.
admin.site.register(Case)
admin.site.register(Files)
admin.site.register(JointUser)

admin.site.register(CompanyInfo)
admin.site.register(Dependant)
admin.site.register(DirectorShareholder)
admin.site.register(Adverse)
admin.site.register(Property)


@admin.register(ApplicantDetails)
class ApplicantDetailsAdmin(admin.ModelAdmin):
    list_display = ("alias", "created_at", "updated_at", "applicant")
