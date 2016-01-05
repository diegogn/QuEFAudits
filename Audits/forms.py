__author__ = 'Diego Desarrollo'
from django import forms
from Audits.models import Audit, Tag, Item, Document, Answer, Instance
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q


class AuditForm(forms.ModelForm):
    plan = (
        (0, _("No needed")),
        (1, _("One time in week")),
        (2, _("One time in month")),
        (3, _("One time in year")),
        (4, _("Advanced Configuration")),
    )

    period = forms.ChoiceField(label=_("Execution time"), choices=plan)

    def __init__(self, *args, **kwargs):
        super(AuditForm, self).__init__(*args, **kwargs)
        self.fields['auditor'].queryset = User.objects.filter(user_permissions__codename__exact='auditor')
        self.fields['usuario'].queryset = User.objects.filter(user_permissions__codename__exact='user')
        self.fields['start_date'].widget = forms.DateInput(attrs={'placeholder': _("DD/MM/YYYY")})

    class Meta:
        model = Audit
        exclude = ['eventId', 'gestor', 'state', 'creation_date']


class UserForm(UserCreationForm):
    rol = (
        (1, _('Admins')),
        (2, _('Gestors')),
        (3, _('Users')),
        (4, _('Auditors')),
    )

    name = forms.CharField(label=_('Name'))
    surname = forms.CharField(label=_('Surname'))
    email = forms.EmailField(label=_('Email'))
    rol = forms.ChoiceField(label=_('Rol'), choices=rol)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']

        rol = self.cleaned_data['rol']
        if rol == '1':
            permission = Permission.objects.get(codename='admin')
        elif rol == '2':
            permission = Permission.objects.get(codename='gestor')
        elif rol == '3':
            permission = Permission.objects.get(codename='user')
        elif rol == '4':
            permission = Permission.objects.get(codename='auditor')

        if commit:
            user.save()
            user.user_permissions.add(permission)
        return user


class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Tag
        fields = ('name', 'parent', 'weight', 'public')


class TagEditForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name', 'weight')


class ItemCreateForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = ['tag']


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = ['item', 'instance']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('name','value')


class InstanceForm(forms.ModelForm):
    class Meta:
        model = Instance
        fields = ('level',)
