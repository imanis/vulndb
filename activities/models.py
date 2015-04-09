from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape


class Activity(models.Model):
    FAVORITE = 'F'
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )

    user = models.ForeignKey(User)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.IntegerField(null=True, blank=True)
    question = models.IntegerField(null=True, blank=True)
    answer = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __unicode__(self):
        return self.activity_type


# def save(self, *args, **kwargs):
# super(Activity, self).save(*args, **kwargs)
#        if self.activity_type == Activity.FAVORITE:
#            Question = models.get_model('questions', 'Question')
#            question = Question.objects.get(pk=self.question)
#            user = question.user
#            user.profile.reputation = user.profile.reputation + 5
#            user.save()

class Notification(models.Model):
    COMMENTED = 'C'
    ALSO_COMMENTED = 'S'
    EDITED_PROJECT = 'E'
    ADDING_VULN = 'V'
    ADDING_VULNINST = 'I'
    ADDING_VULN_TO_PROJECT = 'P'
    NOTIFICATION_TYPES = (

        (COMMENTED, 'Commented'),
        (ALSO_COMMENTED, 'Also Commented'),
        (EDITED_PROJECT, 'Edited Project'),
        (ADDING_VULN, 'Adding Vulnerability'),
        (ADDING_VULNINST, 'Adding Vulnerability Instance'),
        (ADDING_VULN_TO_PROJECT, 'Adding new Vulnerability to project'),
    )

    _COMMENTED_TEMPLATE = u'<a href="/{0}/">{1}</a> commented on your activity: <a href="/feeds/{2}/">{3}</a>'
    _ALSO_COMMENTED_TEMPLATE = u'<a href="/{0}/">{1}</a> also commentend on the activity: <a href="/feeds/{2}/">{3}</a>'
    _EDITED_PROJECT_TEMPLATE = u'<a href="/{0}/">{1}</a> edited a project you are participated in: <a href="/projects/{2}/">{3}</a>'
    _ADDING_VULN_TEMPLATE = u'<a href="/{0}/">{1}</a> Add a new Vuln  <a href="/vulns/{2}/">{3}</a> to the Database'
    _ADDING_VULNINST_TEMPLATE = u'<a href="/{0}/">{1}</a> load a new Vuln  <a href="/vulns/{2}/">{3}</a> to <a href="/projects/{4}/">{5}</a>  '
    _ADDING_VULN_TO_PROJECT_TEMPLATE = u'<a href="/{0}/">{1}</a> Add unexisting  Vuln  <a href="/projects/show/{2}/">{3}</a> to <a href="/projects/{4}/">{5}</a>  '

    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    date = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey('feeds.Feed', null=True, blank=True)
    vuln = models.ForeignKey('vulns.Vuln', null=True, blank=True)
    vulni = models.ForeignKey('projects.VulnInst', null=True, blank=True)
    project = models.ForeignKey('projects.Project', null=True, blank=True)
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return u'{0}...'.format(value[:summary_size])
        else:
            return value

    def __unicode__(self):

        if self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
            )

        elif self.notification_type == self.ALSO_COMMENTED:
            return self._ALSO_COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
            )
        elif self.notification_type == self.EDITED_PROJECT:
            return self._EDITED_PROJECT_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.article.slug,
                escape(self.get_summary(self.article.title))
            )
        elif self.notification_type == self.ADDING_VULN:
            return self._ADDING_VULN_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.vuln.slug,
                escape(self.get_summary(self.vuln.vulnerability))
            )

        elif self.notification_type == self.ADDING_VULNINST:
            return self._ADDING_VULNINST_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.vulni.slug,
                escape(self.get_summary(self.vulni.vulnerability)),
                self.project.slug,
                self.project.project
            )
        
        elif self.notification_type == self.ADDING_VULN_TO_PROJECT:
            return self._ADDING_VULN_TO_PROJECT_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.vulni.pk,
                escape(self.get_summary(self.vulni.vulnerability)),
                self.project.slug,
                self.project.project
            )
        else:
            return 'Ooops! Something went wrong.'

