from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from django.template.defaultfilters import slugify
from vulnDB.vulns.models import Tag, Vuln, VulnActionPriorityMatrix, VulnExploitation_complexity, VulnExploitation_impact, VulnAction_complexity,  VulnCategory, VulnSeverityMatrix, VulnType
from django.conf import settings
import os.path


#### The Project Model : The Model that represent a Project

class Project(models.Model):
    #Status of a project
    ACTIVE = 'A'
    ARCHIVED = 'R'
    STATUS = (
        (ACTIVE, 'Active'),
        (ARCHIVED, 'Archived'),
    )
    #Hide Fields
    status = models.CharField(max_length=1, choices=STATUS, default=ACTIVE)
    create_user = models.ForeignKey(User, related_name='create_user')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(User, null=True, blank=True, related_name="+")
    slug = models.SlugField(max_length=255, null=True, blank=True)
    ## Buisness Fields
        # Added by user
    project = models.CharField(max_length=255)
    nature = models.ForeignKey('ProjectNature')
    client = models.ForeignKey('Client')
    teammanager = models.ForeignKey(User,related_name='manager')
    team = models.ManyToManyField(User, blank=True, null=True, related_name='team')


    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ("-create_date",)
    def __unicode__(self):
        return self.project

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Project, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = "%s %s" % (self.pk, self.project.lower())
            self.slug = slugify(slug_str)
        super(Project, self).save(*args, **kwargs)
    @staticmethod
    def get_active():
        projects = Project.objects.filter(status=Project.ACTIVE)
        return projects
    @staticmethod
    def get_archived():
        projects = Project.objects.filter(status=Project.ARCHIVED)
        return projects
    def get_vulns_count(self):
        return VulnInst.objects.filter(project=self).count()
    def get_best_pra_count(self):
        return 0


class ProjectNature(models.Model):
    nature = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=True)
    objective =  models.CharField(max_length=1000, null=True, blank=True)
    class Meta:
        verbose_name = _("Project Nature")
        verbose_name_plural = _("Project Natures")

    def __unicode__(self):
        return self.nature

    @staticmethod
    def get_popular_nature():
        vulns = Vuln.objects.filter(status=Vuln.PUBLISHED)
        count = {}
        for v in vulns:
            if v.nature.nature in count:
                count[v.nature.nature] = count[v.nature.nature] + 1
            else:
                count[v.nature.nature] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]


class VulnInst(models.Model):


    #Hide Fields
    base_pk = models.IntegerField(blank=True,null=True)
    ref = models.CharField(max_length=255,blank=True, null=True, default='ref')
    create_user = models.ForeignKey(User,blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(User, null=True, blank=True, related_name="+")
    slug = models.SlugField(max_length=255, null=True, blank=True)

    ## Buisness Fields
        # Added by user
    vulnerability = models.CharField(max_length=255)
    category = models.ForeignKey(VulnCategory,blank=True, null=True)
    #affected_item =  models.ForeignKey('VulnItem')
    type =  models.ForeignKey(VulnType,blank=True,null=True)
    

    nature =  models.ForeignKey('ProjectNature',blank=True, null=True)
    description = models.TextField(max_length=8000)
    tagsproject = models.ManyToManyField(Tag)
    recommendation =  models.TextField(max_length=4000)
    exploitation_impact = models.ForeignKey('ProjectExploitation_impact',blank=True, null=True)
    exploitation_complexity = models.ForeignKey('ProjectExploitation_complexity',blank=True, null=True)
    action_complexity = models.ForeignKey('ProjectAction_complexity',blank=True, null=True)
   

   #One to Many Relation
    project = models.ForeignKey('Project',blank=True,null=True)


    class Meta:
        unique_together= ('id', 'project')
        verbose_name = _("Vulnerability instance")
        verbose_name_plural = _("Vulnerabilities instances")
        ordering = ("-create_date",)
    def __unicode__(self):
        return ('Instance of %d', self.base_pk  )
    def instanciate(self, vuln):
        self.create_user=vuln.create_user
        self.create_date=vuln.create_date 
        self.type=vuln.type 
        self.update_date=vuln.create_date
        self.slug=vuln.slug
        self.update_user=vuln.update_user
        self.vulnerability=vuln.vulnerability
        self.category=vuln.category
        self.nature=vuln.nature
        self.description=vuln.description
        self.recommendation=vuln.recommendation

    def save(self, *args, **kwargs):
        if not self.pk:
            super(VulnInst, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = "%s %s" % (self.pk, self.vulnerability.lower())
            self.slug = slugify(slug_str)
        super(VulnInst, self).save(*args, **kwargs)
    def get_summary(self):
        if len(self.description) > 255:
            return u'{0}...'.format(self.description[:255])
        else:
            return self.description
    def get_severity(self):
        return ProjectSeverityMatrix.objects.get(exploitation_complexity=self.exploitation_complexity,exploitation_impact=self.exploitation_impact).severity
    def get_action_priority(self):
        return ProjectActionPriorityMatrix.objects.get(action_complexity=self.action_complexity,severity=self.get_severity).action_priority

     #update tag
    def create_tags(self, tags):
        for tag in tags[1:-1].split(","):
                t, created=Tag.objects.get_or_create(name=tag[1:-1].lower())
                self.tagsproject.add(t)
    #update tag
    def get_items_tags(self):
        return [ i.name  for i in self.tagsproject.all()]


class Client(models.Model):
    name = models.CharField(max_length=255)

    def get_picture(self):
        no_picture = settings.STATIC_URL + 'img/client.png'
        try:
            filename = settings.MEDIA_ROOT + '/client_pictures/{0}.jpg'.format(self.pk )
            picture_url = settings.MEDIA_URL +'client_pictures/{0}.jpg'.format(self.pk )
            if os.path.isfile(filename):
                return picture_url
            else:
                return no_picture
        except Exception, e:
            return no_picture

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __unicode__(self):
        return self.name




#####CVSS Models for project add  foreingkey(project) to every model

class ProjectExploitation_impact(models.Model):
    exploitation_impact = models.CharField(max_length=500)
    project = models.ForeignKey(Project, null=True, blank=True)
    color =models.CharField(max_length=10)
    class Meta:
        ordering = ['id']
        verbose_name = _("Exploitation impact")
        verbose_name_plural = _("Exploitation impacts")
    def __unicode__(self):
        return self.exploitation_impact
        


class ProjectExploitation_complexity(models.Model):
        exploitation_complexity = models.CharField(max_length=500)
        project = models.ForeignKey(Project, null=True, blank=True)
        color =models.CharField(max_length=10)

        class Meta:
            ordering = ['id']
            verbose_name = _("Exploitation complexity")
            verbose_name_plural = _("Exploitation complexities")

        def __unicode__(self):
            return self.exploitation_complexity

class ProjectAction_complexity(models.Model):
        action_complexity = models.CharField(max_length=500)
        project = models.ForeignKey(Project, null=True, blank=True)
        color =models.CharField(max_length=10)

        class Meta:
            verbose_name = _("Action complexity")
            verbose_name_plural = _("Action complexities")

        def __unicode__(self):
            return self.action_complexity



class ProjectSeverity(models.Model):
        severity = models.CharField(max_length=25)
        project = models.ForeignKey(Project, null=True, blank=True)
        color =models.CharField(max_length=10)

        class Meta:
            verbose_name = _("severity")
            verbose_name_plural = _("severitys")

        def __unicode__(self):
            return self.severity

class ProjectSeverityMatrix(models.Model):
   
    exploitation_complexity = models.ForeignKey('ProjectExploitation_complexity')
    exploitation_impact = models.ForeignKey('ProjectExploitation_impact')
    severity = models.ForeignKey('ProjectSeverity')
    project = models.ForeignKey(Project, null=True, blank=True)
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

class ProjectAction_priority(models.Model):
        action_priority = models.CharField(max_length=500)
        project = models.ForeignKey(Project, null=True, blank=True)
        color =models.CharField(max_length=10)

        class Meta:
            verbose_name = _("Action priority")
            verbose_name_plural = _("Action priorities")

        def __unicode__(self):
            return self.action_priority



class ProjectActionPriorityMatrix(models.Model):
    action_complexity = models.ForeignKey('ProjectAction_complexity')
    severity = models.ForeignKey('ProjectSeverity')
    action_priority =models.ForeignKey('ProjectAction_priority')
    project = models.ForeignKey(Project, null=True, blank=True)
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