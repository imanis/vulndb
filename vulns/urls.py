from django.conf.urls import patterns, include, url

urlpatterns = patterns('vulnDB.vulns.views',
                       url(r'^$', 'vulns', name='vulns'),
                       url(r'^drafts/$', 'drafts', name='drafts'),
                       url(r'^index/category/(?P<cat_name>.+)/$', 'index_category', name='index_category'),
                       url(r'^index/type/(?P<type_name>.+)/$', 'index_type', name='index_type'),
                       url(r'^index/nature/(?P<nature_name>.+)/$', 'index_nature', name='index_nature'),
                       url(r'^preview/$', 'preview', name='preview'),
                       url(r'^tag/(?P<tag_name>.+)/$', 'item_tag', name='item_tag'),
                       url(r'^add/$', 'add', name='add'),
                       url(r'^edit/(?P<id>\d+)/$', 'edit', name='edit_vuln'),
                       url(r'^delete/(?P<id>\d+)/$', 'delete', name='delete_vuln'),

                       # url(r'^add_category/$', 'add_category', name='add_category'),
                       # url(r'^add_category/$', 'add_category', name='add_category'),
                       # url(r'^comment/$', 'comment', name='comment'),

                       url(r'^preferences/(?P<etat>\w+)/$', 'preferences', name='preferences'),
                       url(r'^change_serevity/(?P<serevety_id>\d+)/$', 'change_serevity', name='change_serevity'),
                       url(r'^change_action/(?P<action_id>\d+)/$', 'change_action', name='change_action'),

                       # update
                       url(r'^action_add/(?P<action>\w+)/$', 'action_add', name='action_add'),
                       url(r'^action_delete/(?P<id>\d+)/(?P<action>\w+)/$', 'action_delete', name='action_delete'),
                       url(r'^action_edit/(?P<id>\d+)/(?P<action>\w+)/$', 'action_edit', name='action_edit'),


                       url(r'^(?P<slug>[-\w]+)/$', 'vuln', name='vuln'),

)