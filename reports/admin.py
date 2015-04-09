from django.contrib import admin
from vulnDB.reports.models import *

admin.site.register(Report)
admin.site.register(ReportTemplate)
admin.site.register(ReportContact)

admin.site.register(TemplateFrontCoverPage)
admin.site.register(TemplateHeader)
admin.site.register(TemplateFooter)
admin.site.register(TemplateFontSize)
admin.site.register(TemplateFont)
