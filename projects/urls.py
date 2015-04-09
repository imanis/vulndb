from django.conf.urls import patterns, include, url

urlpatterns = patterns('vulnDB.projects.views',
                       url(r'^preview/$', 'preview_vuln', name='p_preview_vuln'),

                       url(r'^preferences_project/(?P<project_id>\d+)/(?P<etat>\w+)$', 'preferences',
                           name='preferences_project'),
                       url(r'^add_client/$', 'add_client', name='add_client'),
                       url(r'^chart_data_json/$', 'chart_data_json', name='chart_data_json'),
                       url(r'^all$', 'all', name='all'),
                       url(r'^active$', 'active', name='active'),
                       url(r'^archived$', 'archived', name='archived'),
                       url(r'^start/$', 'start', name='start'),
                       url(r'^modify/(?P<id>\d+)/$', 'modify', name='modify_project'),
                       url(r'^remove/(?P<id>\d+)/$', 'remove', name='remove_project'),
                       url(r'^archive/(?P<id>\d+)/$', 'archive', name='archive_project'),
                       url(r'^activate/(?P<id>\d+)/$', 'activate', name='activate_project'),

                       url(r'^(?P<slug>[-\w]+)/$', 'project', name='project'),
                       url(r'^load$', 'load', name='load'),
                       url(r'^add$', 'add', name='p_add_vuln'),


                       url(r'^edit/(?P<id>\d+)/$', 'edit', name='p_edit_vuln'),
                       url(r'^delete/(?P<id>\d+)/$', 'delete', name='p_delete_vuln'),
                       url(r'^show/(?P<pk>[-\w]+)/$', 'show_vuln', name='p_show_vuln'),
                       url(r'^client/(?P<id>\d+)/$', 'client', name='client'),
                       url(r'^client/c_upload_picture', 'c_upload_picture', name='c_upload_picture'),
                       url(r'^client/c_save_uploaded_picture$', 'c_save_uploaded_picture',
                           name='c_save_uploaded_picture'),
                       url(r'^$', 'projects', name='projects'),

                       url(r'^project_change_serevity/(?P<serevety_id>\d+)/(?P<project_id>\d+)$',
                           'project_change_serevity', name='project_change_serevity'),
                       url(r'^project_change_action/(?P<action_id>\d+)/(?P<project_id>\d+)$', 'project_change_action',
                           name='project_change_action'),

                       # update
                       url(r'^project_action_add/(?P<action>\w+)/$', 'project_action_add', name='project_action_add'),
                       url(r'^project_action_delete/(?P<id>\d+)/(?P<action>\w+)/$', 'project_action_delete',
                           name='project_action_delete'),
                       url(r'^project_action_edit/(?P<id>\d+)/(?P<action>\w+)/$', 'project_action_edit',
                           name='project_action_edit'),
)
