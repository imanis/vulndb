from django.conf.urls import patterns, include, url

urlpatterns = patterns('vulnDB.reports.views',

                       url(r'^$', 'reports', name='reports'),

                       url(r'^templates$', 'templates', name='templates'),

                       url(r'^add_template$', 'add_template',
                           name='add_template'),
                       url(r'^delete_template/(?P<id>\d+)$',
                           'delete_template', name='delete_template'),
                       url(r'^edite_template/(?P<id>\d+)$',
                           'edite_template', name='edite_template'),
                       url(r'^select_template/(?P<id>\d+)$',
                           'select_template', name='select_template'),
                       url(r'^add_frontcover/$', 'add_frontcover',
                           name='add_frontcover'),
                       url(r'^add_font/$', 'add_font', name='add_font'),
                       url(r'^add_footer/$', 'add_footer', name='add_footer'),
                       url(r'^add_header/$', 'add_header', name='add_header'),
                       url(r'^add_font_size/$', 'add_font_size',
                           name='add_font_size'),

                       url(r'^add_report$', 'add_report', name='add_report'),
                       url(r'^add_contact/$', 'add_contact',
                           name='add_contact'),
                       url(r'^delete_report/(?P<id>\d+)$',
                           'delete_report', name='delete_report'),
                       url(r'^edite_report/(?P<id>\d+)$',
                           'edite_report', name='edite_report'),

                       url(r'^generate/(?P<id>\d+)$',
                           'generate', name='generate'),


                       url(r'^add_template_standart$', 'add_template_standart',
                           name='add_template_standart'),
                       url(r'^edite_template_standart$',
                           'edite_template_standart',
                           name='edite_template_standart'),

)
