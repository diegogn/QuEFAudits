from django.contrib import admin
from Audits.models import *

# Register your models here.
admin.site.register(Audit)
admin.site.register(Item)
admin.site.register(Tag)
admin.site.register(Document)
admin.site.register(Instance)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(CredentialsModel)