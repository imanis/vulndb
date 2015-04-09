from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'vulnDB.core.views.home', name='home'),
    url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'core/cover.html'}, name='login'),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^signup/$', 'vulnDB.auth.views.signup', name='signup'),
    url(r'^settings/$', 'vulnDB.core.views.settings', name='settings'),
    url(r'^settings/picture/$', 'vulnDB.core.views.picture', name='picture'),
    url(r'^settings/upload_picture/$', 'vulnDB.core.views.upload_picture', name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', 'vulnDB.core.views.save_uploaded_picture', name='save_uploaded_picture'),
    url(r'^settings/password/$', 'vulnDB.core.views.password', name='password'),
    url(r'^network/$', 'vulnDB.core.views.network', name='network'),
    url(r'^feeds/', include('vulnDB.feeds.urls')),
    url(r'^vulns/', include('vulnDB.vulns.urls')),
    url(r'^reports/', include('vulnDB.reports.urls')),
    url(r'^projects/', include('vulnDB.projects.urls')),
    url(r'^messages/', include('vulnDB.messages.urls')),
    url(r'^notifications/$', 'vulnDB.activities.views.notifications', name='notifications'),
    url(r'^notifications/last/$', 'vulnDB.activities.views.last_notifications', name='last_notifications'),
    url(r'^notifications/check/$', 'vulnDB.activities.views.check_notifications', name='check_notifications'),
    url(r'^search/$', 'vulnDB.search.views.search', name='search'),
    url(r'^(?P<username>[^/]+)/$', 'vulnDB.core.views.profile', name='profile'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
    url(r'^ckeditor/', include('ckeditor.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
