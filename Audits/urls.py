from django.conf.urls import include, url
from Audits import views

urlpatterns = [
    url(r'^create/audit/$', views.create_audit, name='create_audit'),
    url(r'^edit/gestor/audit/(?P<audit_id>[0-9]+)$', views.edit_audit, name='edit_audit'),
    url(r'^delete/gestor/audit/(?P<audit_id>[0-9]+)$', views.delete_audit, name='delete_audit'),
    url(r'^create/user/$', views.create_user, name='create_user'),
    url(r'^list/audits/$', views.list_audits, name='list_audits'),
    url(r'^create/tag/$', views.create_tag, name='create_tag'),
    url(r'^list/tags/(?P<tag_id>[0-9]*)$', views.list_tags, name='list_tags'),
    url(r'^list/gestor/audits/$', views.list_my_audits, name='list_my_audits'),
    url(r'^audit/details/(?P<audit_id>[0-9]+)$', views.audit_details, name='audit_details'),
    url(r'audit/change/state/(?P<audit_id>[0-9]+)$', views.audit_change_state, name='change_audit_state'),
    url(r'^create/gestor/item/(?P<tag_id>[0-9]+)$', views.create_item_no_form, name='create_item'),
    url(r'^list/gestor/items/(?P<tag_id>[0-9]+)$', views.list_tag_items, name='list_tag_items'),
    url(r'^item/gestor/details/(?P<item_id>[0-9]+)$', views.item_details, name='item_details'),
    url(r'^document/create/(?P<item_id>[0-9]+)$', views.create_document, name='create_document'),
    url(r'^document/delete/(?P<document_id>[0-9]+)$', views.document_delete, name='delete_document'),
    url(r'^list/gestor/tags_tree$', views.list_tag_tree, name='list_tags_tree'),
    url(r'^edit/gestor/tag/(?P<tag_id>[0-9]+)$', views.edit_tag, name='edit_tag'),
    url(r'^delete/gestor/tag/(?P<tag_id>[0-9]+)$', views.delete_tag, name='delete_tag'),
    url(r'^edit/gestor/item/(?P<item_id>[0-9]+)$', views.edit_item, name='edit_item'),
    url(r'^delete/gestor/item/(?P<item_id>[0-9]+)$', views.delete_item, name='delete_item'),
    url(r'^create/gestor/answer/(?P<item_id>[0-9]+)$', views.create_answer, name='create_answer'),
    url(r'^edit/gestor/answer/(?P<answer_id>[0-9]+)$', views.edit_answer, name='edit_answer'),
    url(r'^delete/gestor/answer/(?P<answer_id>[0-9]+)$', views.delete_answer, name='delete_answer'),
    url(r'^not_user_permission/$', views.not_user_permission),
    #Urls de usuario
    url(r'^list/user/audits/$', views.list_user_audits, name='user_audits'),
    url(r'^create/instance/(?P<audit_id>[0-9]+)$', views.create_instance, name='create_instance')
]
