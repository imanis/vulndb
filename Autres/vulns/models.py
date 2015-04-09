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
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
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
    nature =  models.ForeignKey('ProjectNature')
    description = models.TextField(max_length=8000)
    recommendation =  models.TextField(max_length=4000)
    exploitation_impact = models.ForeignKey('VulnExploitation_impact')
    exploitation_complexity = models.ForeignKey('VulnExploitation_complexity')
    action_complexity = models.ForeignKey('VulnAction_complexity')
        # Automatic Fields
    severity = models.CharField(max_length=255,blank=True, null=True)
    action_priority = models.CharField(max_length=255,blank=True, null=True)


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

    def create_items_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            if tag:
                t, created = VulnItem.objects.get_or_create(tag=tag.lower(), vuln=self)

    def get_items_tags(self):
        return VulnItem.objects.filter(vuln=self)



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
'''
class VulnItem(models.Model):
    item = models.CharField(max_length=500)

    class Meta:
        verbose_name = _("Affected item")
        verbose_name_plural = _("Affected items")

    def __unicode__(self):
        return self.item

    @staticmethod
    def get_popular_items():
        vulns = Vuln.objects.filter(status=Vuln.PUBLISHED)
        count = {}
        for v in vulns:
            if v.affected_item in count:
                count[v.affected_item.category] = count[v.affected_item.category] + 1
            else:
                count[v.affected_item.catergory] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]
'''

class VulnItem(models.Model):
    tag = models.CharField(max_length=50)
    vuln = models.ForeignKey(Vuln)

    class Meta:
        verbose_name = _('Affected item')
        verbose_name_plural = _('Affected items')
        unique_together = (('tag', 'vuln'),)
        index_together = [['tag', 'vuln'],]

    def __unicode__(self):
        return self.tag

    @staticmethod
    def get_popular_tags():
        tags = VulnItem.objects.all()
        count = {}
        for tag in tags:
            if tag.vuln.status == Vuln.PUBLISHED:
                if tag.tag in count:
                    count[tag.tag] = count[tag.tag] + 1
                else:
                    count[tag.tag] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]

class VulnType(models.Model):
    type = models.CharField(max_length=500)

    class Meta:
        verbose_name = _("Type")
        verbose_name_plural = _("Types")

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

        class Meta:
            verbose_name = _("Exploitation impact")
            verbose_name_plural = _("Exploitation impacts")

        def __unicode__(self):
            return self.exploitation_impact

class VulnExploitation_complexity(models.Model):
        exploitation_complexity = models.CharField(max_length=500)

        class Meta:
            verbose_name = _("Exploitation complexity")
            verbose_name_plural = _("Exploitation complexities")

        def __unicode__(self):
            return self.exploitation_complexity

class VulnAction_complexity(models.Model):
        action_complexity = models.CharField(max_length=500)

        class Meta:
            verbose_name = _("Action complexity")
            verbose_name_plural = _("Action complexities")

        def __unicode__(self):
            return self.action_complexity

class VulnAction_priority(models.Model):
        action_priority = models.CharField(max_length=500)

        class Meta:
            verbose_name = _("Action priority")
            verbose_name_plural = _("Action priorities")

        def __unicode__(self):
            return self.action_priority


class VulnSeverityMatrix(models.Model):
    exploitation_complexity = models.ForeignKey('VulnExploitation_complexity')
    exploitation_impact = models.ForeignKey('VulnExploitation_impact')
    severity =models.CharField(max_length=500)
    class Meta:
        verbose_name = _("Severity rule")
        verbose_name_plural = _("Severity rules")

    def __unicode__(self):
        return  '%s - %s -> %s' %(self.exploitation_complexity , self.exploitation_impact, self.severity)
    @staticmethod
    def get_rule(ex_comp, ex_imp):
        s = VulnSeverityMatrix.objects.filter(exploitation_complexity=ex_comp,exploitation_impact=ex_imp).first()
        if s:
            return s.severity
        else:
            return 'n.a'

class VulnActionPriorityMatrix(models.Model):
    action_complexity = models.ForeignKey('VulnAction_complexity')
    severity = models.CharField(max_length=500)
    action_priority =models.CharField(max_length=500)
    class Meta:
        verbose_name = _("Action priority rule")
        verbose_name_plural = _("Action priority rules")

    def __unicode__(self):
        return  '%s - %s -> %s' %(self.action_complexity , self.severity, self.action_priority)
    @staticmethod
    def get_rule(ac_comp, sev):
        ap = VulnActionPriorityMatrix.objects.filter(action_complexity=ac_comp,severity=sev).first()
        if ap:
            return ap.action_priority
        else:
            return 'n.a'