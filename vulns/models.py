from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from django.template.defaultfilters import slugify
import markdown


#### The Vul Model : The Model that represent a Vulnerability
class Vuln(models.Model):

    #Status of a vuln
    DRAFT = 'D'
    PUBLISHED = 'P'
    PROJECT = 'R'

    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (PROJECT, 'Project'),
    )

    #Hide Fields
    ref = models.CharField(max_length=255,blank=True, null=True, default='ref')
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(User, null=True, blank=True, related_name="+")
    slug = models.SlugField(max_length=255, null=True, blank=True)

    ## Buisness Fields
        # Added by user
    vulnerability = models.CharField(max_length=255)
    category = models.ForeignKey('VulnCategory')
    #affected_item =  models.ForeignKey('VulnItem')
    type =  models.ForeignKey('VulnType')
    #nature =  models.ForeignKey('VulnNature')
    nature =  models.ForeignKey('projects.ProjectNature')

    description = models.TextField(max_length=8000)
    tags = models.ManyToManyField('Tag', verbose_name=_("Affected items"))
    recommendation =  models.TextField(max_length=4000)
    exploitation_impact = models.ForeignKey('VulnExploitation_impact', null=True, blank=True,on_delete=models.SET_NULL)
    exploitation_complexity = models.ForeignKey('VulnExploitation_complexity', null=True, blank=True,on_delete=models.SET_NULL)
    action_complexity = models.ForeignKey('VulnAction_complexity', null=True, blank=True,on_delete=models.SET_NULL)
        # Automatic Fields
    #severity = models.CharField(max_length=255,blank=True, null=True)



    class Meta:
        verbose_name = _("Vulnerability")
        verbose_name_plural = _("Vulnerabilities")
        ordering = ("-create_date",)

    def __unicode__(self):
        return self.vulnerability

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Vuln, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = "%s %s" % (self.pk, self.vulnerability.lower())
            self.slug = slugify(slug_str)
        super(Vuln, self).save(*args, **kwargs)

    def get_content_as_markdown(self):
        return markdown.markdown(self.description, safe_mode='escape')
        #return ck

    def get_severty(self):
    	return VulnSeverityMatrix.objects.get(exploitation_complexity=self.exploitation_complexity,exploitation_impact=self.exploitation_impact).severity

    def get_action_priority(self):
        return VulnActionPriorityMatrix.objects.get(action_complexity=self.action_complexity,severity=self.get_severty).action_priority

    @staticmethod
    def get_published():
        vulns = Vuln.objects.filter(status=Vuln.PUBLISHED)
        return vulns

    def get_recommendation_summary(self):
        if len(self.recommendation) > 20:
            return u'{0}...'.format(self.recommendation[:20])
        else:
            return self.recommendation

    def get_summary(self):
        if len(self.description) > 255:
            return u'{0}...'.format(self.description[:255])
        else:
            return self.description

    def get_summary_as_markdown(self):
        return markdown.markdown(self.get_summary(), safe_mode='escape')

    #update tag
    def create_tags(self, tags):
        for tag in tags[1:-1].split(","):
                t, created=Tag.objects.get_or_create(name=tag[1:-1].lower())
                self.tags.add(t)
    #update tag
    def get_items_tags(self):
        return [ i.name  for i in self.tags.all()]


#Tag model
class Tag(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = _("Vulnerability Item Tag")
        verbose_name_plural = _("Vulnerability Items Tags")
    def __unicode__(self):
        return self.name



#### Category Item and Type of a vuln

class VulnCategory(models.Model):
    category = models.CharField(max_length=500)

    class Meta:
        verbose_name = _("Vulnerability category")
        verbose_name_plural = _("Vulnerability categories")

    def __unicode__(self):
        return self.category

    @staticmethod
    def get_popular_categories():
        vulns = Vuln.objects.filter(status=Vuln.PUBLISHED)
        count = {}
        for v in vulns:
            if v.category.category in count:
                count[v.category.category] = count[v.category.category] + 1
            else:
                count[v.category.category] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]

class VulnType(models.Model):
    type = models.CharField(max_length=500)

    class Meta:
        verbose_name = _("Vulnerability Type")
        verbose_name_plural = _("Vulnerability Types")

    def __unicode__(self):
        return self.type

    @staticmethod
    def get_popular_types():
        vulns = Vuln.objects.filter(status=Vuln.PUBLISHED)
        count = {}
        for v in vulns:
            if v.type.type in count:
                count[v.type.type] = count[v.type.type] + 1
            else:
                count[v.type.type] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]


#####CVSS Models


class VulnExploitation_impact(models.Model):
    exploitation_impact = models.CharField(max_length=500)
    color =models.CharField(max_length=10)

    class Meta:
            ordering = ['id']
            verbose_name = _("Vulnerability Exploitation impact")
            verbose_name_plural = _("Vulnerability Exploitation impacts")

    def __unicode__(self):
        return self.exploitation_impact

class VulnExploitation_complexity(models.Model):
        exploitation_complexity = models.CharField(max_length=500)
        color =models.CharField(max_length=10)

        class Meta:
            ordering = ['id']
            verbose_name = _("Vulnerability Exploitation complexity")
            verbose_name_plural = _("Vulnerability Exploitation complexities")

        def __unicode__(self):
            return self.exploitation_complexity

class VulnAction_complexity(models.Model):
        action_complexity = models.CharField(max_length=500)
        color =models.CharField(max_length=10)

        class Meta:
            ordering = ['id']
            verbose_name = _("Vulnerability Action complexity")
            verbose_name_plural = _("Vulnerability Action complexities")

        def __unicode__(self):
            return self.action_complexity

class VulnSeverity(models.Model):
        severity = models.CharField(max_length=25)
        color =models.CharField(max_length=10)

        class Meta:
            ordering = ['id']
            verbose_name = _("Vulnerability severity")
            verbose_name_plural = _("Vulnerability severities")

        def __unicode__(self):
            return self.severity

class VulnSeverityMatrix(models.Model):

    exploitation_complexity = models.ForeignKey('VulnExploitation_complexity')
    exploitation_impact = models.ForeignKey('VulnExploitation_impact')
    severity = models.ForeignKey('VulnSeverity')
    class Meta:

        verbose_name = _("Vulnerability Severity rule")
        verbose_name_plural = _("Vulnerability Severity rules")

    def __unicode__(self):
        return  '%s - %s -> %s' %(self.exploitation_complexity , self.exploitation_impact, self.severity)
    @staticmethod
    def get_rule(ex_comp, ex_imp):
        s = VulnSeverityMatrix.objects.filter(exploitation_complexity=ex_comp,exploitation_impact=ex_imp).first()
        if s:
            return s.severity
        else:
            return 'n.a'

class VulnAction_priority(models.Model):
        action_priority = models.CharField(max_length=500)
        color =models.CharField(max_length=10)

        class Meta:
            ordering = ['id']
            verbose_name = _("Vulnerability Action priority")
            verbose_name_plural = _("Vulnerability Action priorities")

        def __unicode__(self):
            return self.action_priority

class VulnActionPriorityMatrix(models.Model):
    action_complexity = models.ForeignKey('VulnAction_complexity')
    severity = models.ForeignKey('VulnSeverity')
    action_priority =models.ForeignKey('VulnAction_priority')
    class Meta:
        verbose_name = _("Vulnerability Action priority rule")
        verbose_name_plural = _("Vulnerability Action priority rules")

    def __unicode__(self):
        return  '%s - %s -> %s' %(self.action_complexity , self.severity, self.action_priority)
    @staticmethod
    def get_rule(ac_comp, sev):
        ap = VulnActionPriorityMatrix.objects.filter(action_complexity=ac_comp,severity=sev).first()
        if ap:
            return ap.action_priority
        else:
            return 'n.a'


