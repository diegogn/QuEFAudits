from django.db import models
from django.contrib.auth.models import User
from oauth2client.django_orm import CredentialsField
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class CredentialsModel(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name=_("User"))
    credential = CredentialsField()


class Administrator(models.Model):
    email = models.EmailField(default="a@f.esa")
    name = models.CharField(max_length="50", verbose_name=_("Name"))
    surname = models.CharField(max_length="50", verbose_name=_("Surname"))


class Gestor(models.Model):
    email = models.EmailField(default="a@f.esa")
    name = models.CharField(max_length="50", verbose_name=_("Name"))
    surname = models.CharField(max_length="50", verbose_name=_("Surname"))


class Usuario(models.Model):
    email = models.EmailField(default="a@f.esa")
    name = models.CharField(max_length="50", verbose_name=_("Name"))
    surname = models.CharField(max_length="50", verbose_name=_("Surname"))


class Auditor(models.Model):
    email = models.EmailField(default="a@f.esa")
    name = models.CharField(max_length="50", verbose_name=_("Name"))
    surname = models.CharField(max_length="50", verbose_name=_("Surname"))


class Tag(MPTTModel):
    name = models.CharField(_("Name"), max_length=50)
    #Relaciones
    parent = TreeForeignKey('self', null=True, blank=True, related_name="children", verbose_name=_("Father Tag")
                            , db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Audit(models.Model):
    frecuency = (
        ('DAYLY', _('DAYLY')),
        ('WEAKLY', _('WEAKLY')),
        ('MONTHLY', _('MONTHLY')),
        ('YEARLY', _('YEARLY')),
    )

    name = models.CharField(_("Name"), max_length=100)
    creationDate = models.DateField(_("CreationDate"))
    startDate = models.DateField(_("StartDate"))
    eventId = models.IntegerField(null=True)
    regularityInt = models.IntegerField(_("Regularity"))
    regularity = models.CharField(_("Period"), max_length=100, choices=frecuency)
    #Ahora se definen las relaciones
    gestor = models.ForeignKey(User, related_name='gestor')
    usuario = models.ForeignKey(User, null=True, verbose_name=_("User"), related_name='usuario')
    auditor = models.ForeignKey(User, null=True, verbose_name=_("Auditor"), related_name='auditor')
    tags = models.ManyToManyField('Tag', verbose_name=_("Tags"))

    def __str__(self):
        return self.name


class Instance(models.Model):
    Date = models.DateField(_("Date"))
    #Relaciones
    audit = models.ForeignKey('Audit')
    items = models.ManyToManyField('Item', through='Result', verbose_name=_("Items"))


class Document(models.Model):
    filename = models.CharField(_("Filename"), max_length=100)
    docFile = models.FileField(_("File"), upload_to="Documents/%Y%m%d")
    #Relaciones
    instance = models.ForeignKey('Instance', null=True)
    item = models.ForeignKey('Item', null=True)

    def __str__(self):
        return self.filename;


class Item(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    question = models.CharField(_("Question"), max_length=100)
    url = models.URLField(_("URL"), max_length=200,blank=True)
    #Relaciones
    tag = models.ForeignKey('Tag', verbose_name=_("Tag"))
    def __str__(self):
        return self.name


class Answer(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    value = models.TextField(_("Value"))
    #Relaciones
    item = models.ForeignKey('Item')

    def __str__(self):
        return self.name


class Result(models.Model):
    instance = models.ForeignKey('Instance')
    item = models.ForeignKey('Item')
    answer = models.ForeignKey('Answer', null=True)