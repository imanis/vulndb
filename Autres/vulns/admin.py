from django.contrib import admin
from vulnDB.vulns.models import Vuln, VulnCategory, VulnItem, VulnType, VulnExploitation_complexity, VulnExploitation_impact, VulnAction_complexity, VulnAction_priority, \
    VulnSeverityMatrix, VulnActionPriorityMatrix
from vulnDB.vulns.forms import VulnForm
from django import forms
from django.db import models


class VulnAdmin(admin.ModelAdmin):
    form = VulnForm


admin.site.register(Vuln)
admin.site.register(VulnCategory)
admin.site.register(VulnItem)
admin.site.register(VulnType)
admin.site.register(VulnExploitation_complexity)
admin.site.register(VulnExploitation_impact)
admin.site.register(VulnAction_complexity)
admin.site.register(VulnAction_priority)
admin.site.register(VulnSeverityMatrix)
admin.site.register(VulnActionPriorityMatrix)