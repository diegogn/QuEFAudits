from django import template
from Audits.models import CredentialsModel
from oauth2client.django_orm import Storage

register = template.Library()


@register.filter(name="is_sync")
def is_sync(user):
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    credential = storage.get()

    return not credential is None
