# -*- encoding: utf8 -*-
from django.shortcuts import HttpResponseRedirect, render, get_list_or_404, get_object_or_404
from Audits.forms import AuditForm, UserForm, TagForm, ItemCreateForm, DocumentForm, AnswerForm
from models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from QuEFAudits import settings
from django.contrib.auth.decorators import user_passes_test


# Create your views here.
@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def create_audit(request):
    if request.method == 'POST':
        form = AuditForm(request.POST)
        if form.is_valid():
            audit = form.save(commit=False)
            audit.gestor = request.user
            audit.save()
            form.save_m2m()

            return HttpResponseRedirect('/audits/list/gestor/audits/?page=-1')
    else:
        form = AuditForm()
    return render(request, 'create_audit.html', {'form': form, 'back_url': '/audits/list/gestor/audits/?page=%s' %
                                                                   request.GET.get('page')})


def index(request):
    return render(request, 'welcome.html', {})


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
    audits = Audit.objects.all()
    paginator = Paginator(audits, 25)

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
    audits = Audit.objects.filter(gestor=request.user)
    paginator = Paginator(audits, 25)

    page = request.GET.get('page')

    try:
        audits_page = paginator.page(page);
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
        if form.is_valid():
            tag = form.save()
            return HttpResponseRedirect('/audits/list/gestor/tags_tree')
    else:
        form = TagForm

    return render(request, 'form.html', {'form': form, 'back_url': '/audits/list/gestor/tags_tree'})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def list_tags(request, tag_id):
    tags = Tag.objects.all()

    paginator = Paginator(tags, 25)

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
    return render(request, 'form.html', {'form': form, 'back_url': '/audits/list/gestor/items/'+tag_id+'?page='+request.GET.get('page')})


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

    paginator = Paginator(items, 25)

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
def list_tag_items(request, tag_id):
    items = Item.objects.filter(tag_id=tag_id)
    paginator = Paginator(items, 25)

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
def item_details(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    context = {'item': item}
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.item = item
            file.instance = None
            file.save()
            context['okMessage'] = True
    else:
        form = DocumentForm
    context['form'] = form
    context['formA'] = AnswerForm
    context['page'] = request.GET.get('page')

    return render(request, 'item_details.html', context)


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
    tags = Tag.objects.all()

    return render(request, "list_tags_tree.html", {"tags": tags})

# HttpResponse('<html><title>En contrucción</title><body><h1>En construcción</h1></body></html>')


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def edit_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/audits/list/gestor/tags_tree')
    else:
        form = TagForm(instance=tag)

    return render(request, "form.html", {"form": form, 'back_url': '/audits/list/gestor/tags_tree'})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    tag.delete()

    return HttpResponseRedirect('/audits/list/gestor/tags_tree')


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
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()

    return HttpResponseRedirect('/audits/list/gestor/items/'+item.tag_id)


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

            return HttpResponseRedirect('/audits/item/gestor/details/%s' % item_id)
    else:
        form = AnswerForm

    return render(render,'list_tags.html', {'formA': form, 'back_url': 'audits/item/gestor/details/%s' % item_id})


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

    return render(request, 'form.html', {'form': form, 'back_url': 'audits/item/gestor/details/%s' % answer.item_id})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    id = answer.item.id
    answer.delete()

    return HttpResponseRedirect('/audits/item/gestor/details/%d' % id)