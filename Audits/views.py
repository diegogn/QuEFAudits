# -*- encoding: utf8 -*-
from django.shortcuts import HttpResponseRedirect, render, get_list_or_404, get_object_or_404, HttpResponse
from Audits.forms import AuditForm, UserForm, TagForm, ItemCreateForm, DocumentForm, AnswerForm, TagEditForm, InstanceForm
from models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test_object, permission_required_or
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from QuEFAudits import settings
import time
from django.db.models import Q, Min

#User passes test functions.
def audit_owner(user, kwargs):
    audit_id = kwargs.itervalues().next()
    audit = get_object_or_404(Audit, id=audit_id)

    return audit.gestor == user

def user_audit(user, kwargs):
    audit_id = kwargs.itervalues().next()
    audit = get_object_or_404(Audit, id=audit_id)

    return audit.gestor == user or (audit.usuario == user and audit.state != 'INACTIVE') or \
           (audit.auditor == user and audit.state != 'INACTIVE')


def user_item_owner(user, kwargs):
    item_id = kwargs.itervalues().next()
    item = get_object_or_404(Item, id=item_id)
    return item.tag.create_user == user


def item_tag_public(user, kwargs):
    item_id = kwargs.itervalues().next()
    item = get_object_or_404(Item, id=item_id)
    return item.tag.public or item.tag.create_user == user


def tag_public(user, kwargs):
    tag_id = kwargs.itervalues().next()
    tag = get_object_or_404(Tag, id=tag_id)
    return tag.public or tag.create_user == user


def user_item_tag_delete(user, kwargs):
    item_id = kwargs.itervalues().next()
    item = get_object_or_404(Item, id=item_id)

    return item.tag.create_user == user and item.results.count() == 0

def is_tag_creator(user, kwargs):
    tag_id = kwargs.itervalues().next()
    tag = get_object_or_404(Tag, id=tag_id)

    return tag.create_user == user


# Create your views here.
def not_user_permission(request):
    return render(request,'not_user_permission.html')

def index(request):
    return render(request, 'welcome.html', {})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def create_audit(request):
    if request.method == 'POST':
        form = AuditForm(request.POST)
        form.fields['tags'].queryset = Tag.objects.filter(Q(create_user=request.user) or Q(public=True))
        if form.is_valid():
            audit = form.save(commit=False)
            audit.gestor = request.user
            audit.state = 'INACTIVE'
            audit.creation_date = time.strftime("%Y-%m-%d")
            audit.save()
            form.save_m2m()

            #Como se puede etiquetar una etiqueta padre y una hija este algoritmo elimina esa redundancia.
            for tag in audit.tags.all():
                if tag.parent in audit.tags.all():
                    audit.tags.remove(tag)



            return HttpResponseRedirect('/audits/list/gestor/audits/?page=-1')
    else:
        form = AuditForm()
        form.fields['tags'].queryset = Tag.objects.filter(Q(create_user=request.user) or Q(public=True))
    return render(request, 'create_audit.html', {'form': form, 'back_url': '/audits/list/gestor/audits/?page=%s' %
                                                                   request.GET.get('page')})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
@user_passes_test_object(audit_owner)
def edit_audit(request, audit_id):
    audit = get_object_or_404(Audit, id=audit_id)
    if request.method == 'POST':
        form = AuditForm(request.POST, instance=audit)
        form.fields['tags'].queryset = Tag.objects.filter(Q(create_user=request.user) or Q(public=True))
        if form.is_valid():
            audit = form.save(commit=False)
            audit.gestor = request.user
            audit.state = 'INACTIVE'
            audit.creation_date = time.strftime("%Y-%m-%d")
            audit.save()
            form.save_m2m()

            #Como se puede etiquetar una etiqueta padre y una hija este algoritmo elimina esa redundancia.
            for tag in audit.tags.all():
                if tag.parent in audit.tags.all():
                    audit.tags.remove(tag)
            return HttpResponseRedirect('/audits/audit/details/%d'% audit.id)
    else:
        form = AuditForm(instance=audit)
        form.fields['tags'].queryset = Tag.objects.filter(Q(create_user=request.user) or Q(public=True))

    return render(request, 'edit_audit.html', {'form': form, 'back_url': '/audits/audit/details/%s' % audit_id})

@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
@user_passes_test_object(user_audit)
def delete_audit(request, audit_id):
    audit = get_object_or_404(Audit, id=audit_id)
    if request.method == 'POST':
        if audit.state == 'INACTIVE':
            audit.delete()
            return JsonResponse({"delete": "ok"})
        else:
            return JsonResponse({"delete": "bad"})
    else:
        return JsonResponse({"sorry": "bad method"})

@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.admin', login_url=settings.LOGIN_URL)
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/login/')
    else:
        form = UserForm
    return render(request, 'form.html', {'form': form})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.admin', login_url=settings.LOGIN_URL)
def list_audits(request):
    audits = Audit.objects.filter(~Q(state='ELIMINATED'))
    paginator = Paginator(audits, 12)

    page = request.GET.get('page')

    try:
        audits_page = paginator.page(page)
    except PageNotAnInteger:
        audits_page = paginator.page(1)
    except EmptyPage:
        audits_page = paginator.page(paginator.num_pages)

    return render(request, 'list_audits.html', {'element_page': audits_page})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def list_my_audits(request):
    audits = Audit.objects.filter(Q(gestor=request.user) & ~Q(state='ELIMINATED'))
    paginator = Paginator(audits, 12)

    page = request.GET.get('page')

    try:
        audits_page = paginator.page(page)
    except PageNotAnInteger:
        audits_page = paginator.page(1)
    except EmptyPage:
        audits_page = paginator.page(paginator.num_pages)

    return render(request, 'list_audits.html', {'element_page': audits_page})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        form.fields['parent'].queryset = Tag.objects.filter(create_user=request.user)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.create_user = request.user

            if tag.parent:
                tag.public = tag.parent.public

            tag.save()
            form.save_m2m()

            return HttpResponseRedirect('/audits/list/gestor/tags_tree')
    else:
        form = TagForm()
        form.fields['parent'].queryset = Tag.objects.filter(create_user=request.user)

    return render(request, 'create_tag.html', {'form': form, 'back_url': '/audits/list/gestor/tags_tree'})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
@ensure_csrf_cookie
def list_tags(request, tag_id):
    tags = Tag.objects.all()

    paginator = Paginator(tags, 12)

    page = request.GET.get('page')

    try:
        tags_page = paginator.page(page)
    except PageNotAnInteger:
        tags_page = paginator.page(1)
    except EmptyPage:
        tags_page = paginator.page(paginator.num_pages)

    #Procedo a guardar el form
    context = {'element_page': tags_page}

    if request.method == 'POST':
            a = create_item(request, tag_id)
            if not a:
                context['okMessage'] = True
                context['form'] = ItemCreateForm
            else:
                context['form'] = a
                context['tag_value'] = int(float(tag_id))
    else:
        context['form'] = ItemCreateForm

    return render(request,'list_tags.html', context)


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
@user_passes_test_object(is_tag_creator)
def create_item_no_form(request, tag_id):
    if request.method == 'POST':
        form = ItemCreateForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.tag = get_object_or_404(Tag,id=tag_id)
            item.save()
            return HttpResponseRedirect('/audits/list/gestor/items/'+tag_id+'?page=-1')
    else:
        form = ItemCreateForm
    return render(request, 'create_item.html', {'form': form, 'back_url': '/audits/list/gestor/items/'+tag_id+'?page='+request.GET.get('page')})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def create_item(request, tag_id):
        form = ItemCreateForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.tag = get_object_or_404(Tag,id=tag_id)
            item.save()
        else:
            return form

@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def list_items(request):
    items = Item.objects.all()

    paginator = Paginator(items, 12)

    page = request.GET.get('page')

    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(1)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)

    return render(request,'list_items.html', {'element_page': items_page})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
@user_passes_test_object(tag_public)
def list_tag_items(request, tag_id):
    items = Item.objects.filter(tag_id=tag_id)
    paginator = Paginator(items, 12)

    page = request.GET.get('page')

    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(1)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)

    return render(request,'list_items.html', {'element_page': items_page, 'tag': Tag.objects.get(id=tag_id)})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
@ensure_csrf_cookie
def item_details(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    context={}
    context['item'] = item
    context['form'] = DocumentForm
    context['formA'] = AnswerForm
    context['page'] = request.GET.get('page')

    return render(request, 'item_details.html', context)

@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def create_document(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.item = item
            doc.instance = None
            doc.save()

            response = {}
            response['id'] = doc.id
            response['filename'] = doc.filename
            return JsonResponse(response)
        else:
            return JsonResponse(form.errors)
    else:
        return JsonResponse({"sorry": "bad method"})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def document_delete(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    if document.item:
        iden = document.item.id
    else:
        iden = document.instance.id

    document.delete()

    return HttpResponseRedirect('/audits/item/gestor/details/%d' % iden)

@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def list_tag_tree(request):
    tags = Tag.objects.filter(Q(create_user=request.user) | Q(public=True))

    return render(request, "list_tags_tree.html", {"tags": tags})

# HttpResponse('<html><title>En contrucción</title><body><h1>En construcción</h1></body></html>')


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def edit_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        form = TagEditForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/audits/list/gestor/tags_tree')
    else:
        form = TagEditForm(instance=tag)

    return render(request, "form.html", {"form": form, 'back_url': '/audits/list/gestor/tags_tree'})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
@user_passes_test_object(is_tag_creator)
def delete_tag(request, tag_id):

    if request.method == 'POST':
        tag = get_object_or_404(Tag, id=tag_id)
        tag.delete()

        return JsonResponse({'message': 'ok', 'id': tag_id})
    else:
        return JsonResponse({'sorry': 'bad method'})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemCreateForm(request.POST, instance=item)
        if form.is_valid():
            i = form.save()
            return HttpResponseRedirect('/audits/item/gestor/details/%d' % i.id)
    else:
        form = ItemCreateForm(instance=item)

    return render(request, "form.html", {"form": form, 'back_url': '/audits/item/gestor/details/%s' % item_id})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
@user_passes_test_object(user_item_tag_delete)
def delete_item(request, item_id):

    if request.method == 'POST':
        item = get_object_or_404(Item, id=item_id)
        item.delete()
        return JsonResponse({'message': 'ok', 'tag': item.tag_id})

    else:
        return JsonResponse({'sorry': 'bad method'})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def create_answer(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.item = item
            answer.save()

            response = {}
            response['id'] = answer.id
            response['name'] = answer.name
            response['value'] = answer.value

            return JsonResponse(response)
        else:
            return JsonResponse(form.errors)
    else:
        return JsonResponse({"sorry": "bad method"})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def edit_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/audits/item/gestor/details/%s' % answer.item.id)
    else:
        form = AnswerForm(instance=answer)

    return render(request, 'form.html', {'form': form, 'back_url': '/audits/item/gestor/details/%s' % answer.item_id})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    id = answer.item.id
    answer.delete()

    return HttpResponseRedirect('/audits/item/gestor/details/%d' % id)


@ensure_csrf_cookie
@user_passes_test_object(user_audit)
@login_required(login_url=settings.LOGIN_URL)
@permission_required_or(['auth.gestor', 'auth.user', 'auth.auditor'], login_url=settings.LOGIN_URL)
def audit_details(request, audit_id):
    audit = get_object_or_404(Audit, id=audit_id)
    instances = Instance.objects.filter(audit_id=audit_id)

    paginator = Paginator(instances, 5)

    page = request.GET.get('page')

    try:
        instances_page = paginator.page(page)
    except PageNotAnInteger:
        instances_page = paginator.page(1)
    except EmptyPage:
        instances_page = paginator.page(paginator.num_pages)

    return render(request, 'audit_details.html', {'audit': audit, 'instances': instances_page,
                                                  'pageb': request.GET.get('pageb'),
                                                  'start_instance': audit.instance_set.filter(state='STARTED').count()})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def audit_change_state(request, audit_id):
    audit = get_object_or_404(Audit, id=audit_id)

    if audit.state == 'INACTIVE':
        audit.state = 'ACTIVE'
    elif audit.state == 'ACTIVE':
        audit.state = 'FINISH'
    elif audit.state == 'FINISH':
        audit.state = 'ELIMINATED'

    audit.save()

    return HttpResponseRedirect('/audits/audit/details/' + audit_id)


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.user', login_url=settings.LOGIN_URL)
def list_user_audits(request):
    audits = Audit.objects.filter(Q(usuario=request.user) & ~Q(state='INACTIVE') & ~Q(state='ELIMINATED'))

    paginator = Paginator(audits, 12)

    page = request.GET.get('page')

    try:
        audits_page = paginator.page(page)
    except PageNotAnInteger:
        audits_page = paginator.page(1)
    except EmptyPage:
        audits_page = paginator.page(paginator.num_pages)

    return render(request, 'list_audits.html', {'element_page': audits_page})


def create_instance(request, audit_id):
    audit = get_object_or_404(Audit, id=audit_id)

    if request.method == 'POST':
        form = InstanceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.audit = audit
            instance.state = 'STARTED'
            instance.tags = audit.tags

            #Primero comprobamos que no existe ningún item que no tenga al menos dos respuestas
            for tag in audit.tags.all():
                for item in tag.item_set:
                    if item.answer_set.count() < 2:
                        return render(request, 'item_no_answer.html')

            #Ahora creamos por cada item de las etiquetas un result que servirá para su evaluación
            for tag in audit.tags.all():
                items = tag.item.all()
                items2 = Item.objects.filter(tag_parent=tag)

    else:
        form = InstanceForm

    return render(request, 'form.html', {'form': form, 'back_url': '/audits/audit/details/'+audit_id})


def create_result(item_list, instance):
    for item in item_list:
        answer = Answer.objects.filter(item=item)[0]
        Instance.objects.create(instance=instance, item=item, answer=answer)


def tag_items(tags):
    result = []

    for tag in tags:
        result.extend(Item.objects.filter(tag=tag))

        if tag.children.all().count() > 0:
            tags.extend(tag.children.all())

    return result