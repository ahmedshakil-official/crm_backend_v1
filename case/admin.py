from django.contrib import admin

from case.models import (
    Case,
    Files,
    JointUser,
    ApplicantDetails,
    CompanyInfo,
    Dependant,
    DirectorShareholder,
)

# Register your models here.
admin.site.register(Case)
admin.site.register(Files)
admin.site.register(JointUser)
admin.site.register(ApplicantDetails)
admin.site.register(CompanyInfo)
admin.site.register(Dependant)
admin.site.register(DirectorShareholder)
