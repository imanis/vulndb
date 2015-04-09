from django.conf.urls import patterns, include, url

urlpatterns = patterns('home.views',
                       url(r'^$', 'home', name='home'),
                       url(r'^contact$', 'cantact', name='cantact'),
                       url(r'^qualifications$', 'qualification',
                           name='qualification'),
                       url(r'^metiers$', 'jobs', name='jobs'),
                       url(r'^knx$', 'lnx', name='lnx'),
                       url(r'^societe$', 'company', name='company'),


                       )
