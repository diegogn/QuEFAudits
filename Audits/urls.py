from django.conf.urls import include, url
from Audits import views

urlpatterns = [
    url(r'^create/audit/$', views.create_audit, name='create_audit'),
    url(r'^create/user/$', views.create_user, name='create_user'),
    url(r'^list/audits/$', views.list_audits, name='list_audits'),
    url(r'^create/tag/$', views.create_tag, name='create_tag'),
    url(r'^list/tags/(?P<tag_id>[0-9]*)$', views.list_tags, name='list_tags'),
    url(r'^list/gestor/audits/$', views.list_my_audits, name='list_my_audits'),
    url(r'^create/gestor/item/(?P<tag_id>[0-9]+)$', views.create_item, name='create_item'),
    url(r'^list/gestor/items/(?P<tag_id>[0-9]*)$', views.list_tag_items, name='list_tag_items'),
    url(r'^item/gestor/details/(?P<item_id>[0-9]+)$', views.item_details, name='item_details'),
    url(r'^document/delete/(?P<document_id>[0-9]+)$', views.document_delete, name='delete_document'),
    url(r'^list/gestor/tags_tree$', views.list_tag_tree, name='list_tags_tree'),
]
