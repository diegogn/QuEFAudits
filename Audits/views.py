# -*- encoding: utf8 -*-
from django.shortcuts import HttpResponseRedirect, render, get_list_or_404, get_object_or_404
from Audits.forms import AuditForm, UserForm, TagForm, ItemCreateForm, DocumentForm
from models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from QuEFAudits import settings


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

            return HttpResponseRedirect('/')
    else:
        form = AuditForm()
    return render(request, 'form.html', {'form': form})


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
            return HttpResponseRedirect('/')
    else:
        form = TagForm

    return render(request, 'form.html', {'form': form})


@login_required(login_url=settings.LOGIN_URL)
@permission_required('auth.gestor', login_url=settings.LOGIN_URL)
def list_tags(request, tag_id):
    tags = Tag.objects.all()

    paginator = Paginator(tags, 5)

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
            return HttpResponseRedirect('/')
    else:
        form = ItemCreateForm
    return render(request, 'form.html', {'form': form})


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

    if tag_id:
        items = get_list_or_404(Item, id=tag_id)
    else:
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
# HttpResponse('<html><title>En contrucción</title><body><h1>En construcción</h1></body></html>')

