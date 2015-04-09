from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
# Create your models here.


class Report(models.Model):

    name = models.CharField(max_length=500)
    template = models.ForeignKey('ReportTemplate')
    create_user = models.ForeignKey(User, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    # Filed of a Repport
    contact = models.ForeignKey('ReportContact')

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_reports():
        reports = Report.objects.all()
        return reports


class ReportTemplate(models.Model):

    name = models.CharField(max_length=500)
    create_user = models.ForeignKey(User, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(User, null=True, blank=True, related_name="+")


    front_cover = models.ForeignKey('TemplateFrontCoverPage')
    header = models.ForeignKey('TemplateHeader')
    footer = models.ForeignKey('TemplateFooter')
    font = models.ForeignKey('TemplateFont')
    font_size = models.ForeignKey('TemplateFontSize')

    class Meta:
        verbose_name = _("Report Template")
        verbose_name_plural = _("Report Templates")

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_templates():
        tempates = ReportTemplate.objects.all()
        return tempates


class TemplateFrontCoverPage(models.Model):

    name = models.CharField(max_length=500)
    content = models.TextField(max_length=9000)

    class Meta:
        verbose_name = _("Template Front Cover Page")
        verbose_name_plural = _("Template Front Cover Pages")

    def __unicode__(self):
        return self.name


class TemplateHeader(models.Model):

    name = models.CharField(max_length=500)
    content = models.TextField(max_length=9000)

    class Meta:
        verbose_name = _("Template Header")
        verbose_name_plural = _("Template Headers")

    def __unicode__(self):
        return self.name


class TemplateFooter(models.Model):

    name = models.CharField(max_length=500)
    content = models.TextField(max_length=9000)

    class Meta:
        verbose_name = _("Template Footer")
        verbose_name_plural = _("Template Footers")

    def __unicode__(self):
        return self.name


class TemplateFont(models.Model):

    name = models.CharField(max_length=500)

    class Meta:
        verbose_name = _("Template Font")
        verbose_name_plural = _("Template Fonts")

    def __unicode__(self):
        return self.name


class TemplateFontSize(models.Model):

    size = models.PositiveIntegerField()

    class Meta:
        verbose_name = _("Template Font")
        verbose_name_plural = _("Template Font Sizes")

    def __unicode__(self):
        return str(self.size)


class ReportContact(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField(null=True, blank=True)
    phones = models.CharField(max_length=500)

    class Meta:
        verbose_name = _("Report Contact")
        verbose_name_plural = _("Report Contacts")

    def __unicode__(self):
        return self.name




class ReportTemplateStandart(models.Model):

    name = models.CharField(max_length=500)
    create_user = models.ForeignKey(User, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(User, null=True, blank=True, related_name="+")

    front_cover = models.ForeignKey('TemplateFrontCoverPage')
    header = models.ForeignKey('TemplateHeader')
    footer = models.ForeignKey('TemplateFooter')
    font = models.ForeignKey('TemplateFont')
    font_size = models.ForeignKey('TemplateFontSize')

    class Meta:
        verbose_name = _("Report Template Standart")
        verbose_name_plural = _("Report Templates Standart")

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_templates():
        tempates = ReportTemplate.objects.all()
        return tempates

