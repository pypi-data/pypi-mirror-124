from django.contrib import admin

from huscy.projects import models


class ResearchUnitAdmin(admin.ModelAdmin):
    list_display = 'name', 'code', 'principal_investigator'


admin.site.register(models.Project)
admin.site.register(models.ResearchUnit, ResearchUnitAdmin)
