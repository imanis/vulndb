from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.conf import settings
import os.path
from vulnDB.activities.models import Notification

class Profile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    #reputation = models.IntegerField(default=0)
    #language = models.CharField(max_length=5, default='en')

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:
            url = "http://" + str(self.url)
        return url 

    def get_picture(self):
        no_picture = settings.STATIC_URL + 'img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' + self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' + self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                return no_picture
        except Exception, e:
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    def notify_commented(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.COMMENTED,
                        from_user=self.user,
                        to_user=feed.user,
                        feed=feed).save()

    def notify_also_commented(self, feed):
        comments = feed.get_comments()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != feed.user:
                users.append(comment.user.pk)
        users = list(set(users))
        for user in users:
            Notification(notification_type=Notification.ALSO_COMMENTED,
                from_user=self.user,
                to_user=User(id=user),
                feed=feed).save()

    def notify_Adding_vuln(self, vuln):
        #if self.user != vuln.create_user:
        users = User.objects.exclude( pk=vuln.create_user.pk).all()
        for user in users:
            Notification(notification_type=Notification.ADDING_VULN,
                from_user=self.user,
                to_user=user,
                vuln=vuln).save()


    def notify_Adding_vulnInst(self, vulninst,project):
        #if self.user != vuln.create_user:

        #users = User.objects.exclude( pk=vulninst.create_user.pk).all()
        users = project.team.all()
        for user in users:
            notification = Notification(notification_type=Notification.ADDING_VULNINST,
                from_user=self.user,
                to_user=user,
                vulni=vulninst,
                project=project)
            notification.notification_type = Notification.ADDING_VULNINST
            notification.save()

    def notify_Adding_vuln_to_project(self, vulninst,project):
        #if self.user != vuln.create_user:

        #users = User.objects.exclude( pk=vulninst.create_user.pk).all()
        users = User.objects.filter(groups__name='AdminVulnDB')
        #users = project.get_team()
        for user in users:
            notification = Notification(notification_type=Notification.ADDING_VULN_TO_PROJECT,
                from_user=self.user,
                to_user=user,
                vulni=vulninst,
                project=project)
            notification.notification_type = Notification.ADDING_VULN_TO_PROJECT
            notification.save()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)