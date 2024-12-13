from django.contrib import admin

from case.models import Case, Files, JointUser

# Register your models here.
admin.site.register(Case)
admin.site.register(Files)
admin.site.register(JointUser)
