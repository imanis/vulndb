from django.contrib import admin
from vulnDB.projects.models import *

admin.site.register(Project)
admin.site.register(VulnInst)
admin.site.register(Client)


admin.site.register(ProjectExploitation_impact)
admin.site.register(ProjectExploitation_complexity)
admin.site.register(ProjectAction_complexity)
admin.site.register(ProjectSeverity)
admin.site.register(ProjectSeverityMatrix)
admin.site.register(ProjectAction_priority)
admin.site.register(ProjectActionPriorityMatrix)



admin.site.register(ProjectNature)



