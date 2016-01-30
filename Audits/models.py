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
    weight = models.DecimalField(_("Weight"), max_digits=3, decimal_places=2)
    public = models.BooleanField(_("Public"))
    #Relaciones
    create_user = models.ForeignKey(User, related_name='create_tags', verbose_name=_("Creator"))
    parent = TreeForeignKey('self', null=True, blank=True, related_name="children", verbose_name=_("Father Tag"),
                db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name+'('+str(self.weight)+')'


class Audit(models.Model):
    frecuency = (
        ('DAYLY', _('Dayly')),
        ('WEAKLY', _('Weakly')),
        ('MONTHLY', _('Monthly')),
        ('YEARLY', _('Yearly')),
    )

    state = (
        ('INACTIVE', _('Inactive')),
        ('ACTIVE', _('Active')),
        ('FINISH', _('Finish')),
        ('ELIMINATED', _('Eliminated')),
    )

    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    creation_date = models.DateField(_("CreationDate"))
    start_date = models.DateField(_("StartDate"))
    eventId = models.IntegerField(null=True)
    state = models.CharField(_("State"), max_length=100, choices=state)

    #Ahora se definen las relaciones
    gestor = models.ForeignKey(User, related_name='gestor')
    usuario = models.ForeignKey(User, null=True, verbose_name=_("User"), related_name='usuario')
    auditor = models.ForeignKey(User, null=True, verbose_name=_("Auditor"), related_name='auditor')
    tags = models.ManyToManyField('Tag', verbose_name=_("Tags"))

    #Atributos de la planificacion de google calendar.
    freq = models.CharField(_("Period"), max_length=100, choices=frecuency, null=True, blank=True)
    interval = models.IntegerField(_("Regularity"), null=True, blank=True)
    count = models.IntegerField(_("Count"), null=True, blank=True)
    byday = models.CharField(_("Byday"), max_length=100, null=True, blank=True)
    bymonth = models.CharField(_("Bymonth"), max_length=100, null=True, blank=True)
    bymonthday = models.CharField(_("Bymonthday"), max_length=100, null=True, blank=True)
    wkst = models.CharField(_("Wkst"), max_length=2, null=True, blank=True)
    byyearday = models.CharField(_("Byyearday"), max_length=800, null=True, blank=True)
    bysetpos = models.IntegerField(_("Bysetpos"), null=True, blank=True)

    def __str__(self):
        return self.name


class Instance(models.Model):
    state = (
        ('STARTED', _('Started')),
        ('FINISHED', _('Finished')),
    )

    level = (
        ("LOW", _("Low")),
        ("MEDIUM", _("Medium")),
        ("HIGH", _("High"))
    )

    date = models.DateField(_("Date"))
    state = models.CharField(_("State"), max_length=50, choices=state)
    level = models.CharField(_("Level"), max_length=6, choices=level)
    #Relaciones
    audit = models.ForeignKey('Audit')
    items = models.ManyToManyField('Item', through='Result', verbose_name=_("Items"))
    tags = models.ManyToManyField('Tag', verbose_name=_("Tags"))


class Document(models.Model):
    filename = models.CharField(_("Filename"), max_length=100)
    docFile = models.FileField(_("File"), upload_to="Documents/%Y%m%d")
    #Relaciones
    instance = models.ForeignKey('Instance', null=True)
    item = models.ForeignKey('Item', null=True)

    def __str__(self):
        return self.filename;


class Item(models.Model):
    obligatory = (
        ("SHALL", "shall"),
        ("SHOULD", "should"),
        ("MAY", "may")
    )

    name = models.CharField(_("Name"), max_length=50)
    question = models.TextField(_("Question"))
    url = models.URLField(_("URL"), max_length=200,blank=True)
    obligatory = models.CharField(_("Obligatory"), max_length=6, choices=obligatory)
    #Relaciones
    tag = models.ForeignKey('Tag', verbose_name=_("Tag"))
    def __str__(self):
        return self.name


class Answer(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    value = models.DecimalField(_("Value"), max_digits=3, decimal_places=2)
    #Relaciones
    item = models.ForeignKey('Item')

    def __str__(self):
        return self.name + ': ' + str(self.value)


class Result(models.Model):
    instance = models.ForeignKey('Instance')
    item = models.ForeignKey('Item', related_name='results')
    answer = models.ForeignKey('Answer', null=True)