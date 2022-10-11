from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv, io

from .models import *

def index(request):
    return render(request, 'index.html')


def showEntity(request, id):
    e = get_object_or_404(Entity, pk=id)
    linksfrom = Link.objects.filter(entity1=e).order_by('category__name','entity2__sortkey')
    linksto = Link.objects.filter(entity2=e).order_by('category__name','entity1__sortkey')
    context = { 'entity': e, 'linksfrom': linksfrom, 'linksto': linksto }
    return render(request, 'entity.html', context)


def listEntities(request):
    e = Entity.objects.all().order_by('category','sortkey')
    context = { 'entities' : e }
    return render(request, 'listEntities.html', context)


def searchForm(request):
    return render(request, 'searchForm.html')


def searchName(request):
    term = request.POST.get('termfield','')
    if term == '':
        return redirect('searchForm')
    e = Entity.objects.filter(name__icontains=term)
    context = { 'entities': e }
    return render(request, 'listEntities.html', context)


def search(request):
    term = request.POST.get('termfield','')
    if term == '':
        return redirect('searchForm')
    e = Entity.objects.filter(name__icontains=term) | Entity.objects.filter(url__icontains=term) | Entity.objects.filter(description__icontains=term)
    context = { 'entities': e }
    return render(request, 'listEntities.html', context)


def network(request):
#    e = Entity.objects.all().order_by('category','sortkey')
    e = Entity.objects.filter(category__name='person')
    e = e | Entity.objects.filter(category__name='project')
    e = e | Entity.objects.filter(category__name='site')
    e = e | Entity.objects.filter(category__name='event')
    l = Link.objects.all()
    context = { 'entities' : e, 'links': l }
    return render(request, 'network.html', context)


@login_required
def addEntityForm(request):
    categories = EntityCategory.objects.all().order_by('name')
    context = { 'categories': categories }
    return render(request, 'addEntityForm.html', context )


@login_required
def addEntity(request):
    name = request.POST.get('namefield','no-name')
    sortkey = request.POST.get('sortfield','')
    if sortkey == '':
        sortkey = name
    categoryid = request.POST.get('categoryfield', 0)
    category = get_object_or_404(EntityCategory, pk=categoryid)
    url = request.POST.get('urlfield', '')
    description = request.POST.get('descriptionfield', '')
    e = Entity(name=name, category=category, sortkey=sortkey, url=url, description=description)
    e.save()
    return redirect('showEntity', id=e.id)


@login_required
def editEntityForm(request, id):
    e = get_object_or_404(Entity, pk=id)
    categories = EntityCategory.objects.all().order_by('name')
    context = { 'entity': e, 'categories': categories }
    return render(request, 'editEntityForm.html', context )


@login_required
def editEntity(request):
    id = int(request.POST.get('idfield',0))
    e = get_object_or_404(Entity, pk=id)
    e.name = request.POST.get('namefield','no-name')
    e.sortkey = request.POST.get('sortfield','')
    if e.sortkey == '':
        e.sortkey = e.name
    categoryid = request.POST.get('categoryfield', 0)
    e.category = get_object_or_404(EntityCategory, pk=categoryid)
    e.url = request.POST.get('urlfield', '')
    e.description = request.POST.get('descriptionfield', '')
    e.save()
    return redirect('showEntity', id=id)


@login_required
def addCategoryForm(request):
    categories = EntityCategory.objects.all().order_by('name')
    context = { 'categories': categories }
    return render(request, 'addCategoryForm.html', context)


@login_required
def addCategory(request):
    name = request.POST.get('namefield','no-name')
    e = EntityCategory(name=name)
    e.save()
    return redirect('index')


@login_required
def addLinkCategoryForm(request):
    categories = EntityCategory.objects.all().order_by('name')
    linkcategories = LinkCategory.objects.all().order_by('name')
    context = { 'categories': categories, 'linkcategories': linkcategories }
    return render(request, 'addLinkCategoryForm.html', context)


@login_required
def addLinkCategory(request):
    name = request.POST.get('namefield','no-name')
    category1id = int(request.POST.get('category1field', 0))
    category2id = int(request.POST.get('category2field', 0))
    if category1id == 0:
        category1 = None
    else:
        category1 = get_object_or_404(EntityCategory, pk=category1id)
    if category2id == 0:
        category2 = None
    else:
        category2 = get_object_or_404(EntityCategory, pk=category2id)
    lk = LinkCategory(name=name, entity1Category=category1, entity2Category=category2)
    lk.save()
    return redirect('index')


@login_required
def addLinkForm(request, id):
    e = get_object_or_404(Entity, pk=id)
    categories = LinkCategory.objects.all().order_by('name')
    allentities = Entity.objects.all().order_by('category__name','sortkey')
    context = { 'e': e, 'categories': categories, 'allentities': allentities }
    return render(request, 'addLinkForm.html', context)


@login_required
def addLink(request):
    entity1id = request.POST.get('entity1field', 0)
    entity1 = get_object_or_404(Entity, pk=entity1id)
    entity2id = request.POST.get('entity2field', 0)
    entity2 = get_object_or_404(Entity, pk=entity2id)
    categoryid = request.POST.get('categoryfield', 0)
    category = get_object_or_404(LinkCategory, pk=categoryid)
    l = Link(entity1=entity1, entity2=entity2, category=category)
    l.save()
    return redirect('showEntity',id=entity1id)


@login_required
def importCSVForm(request):
    return render(request, 'importCSVForm.html', {} )


@login_required
def importCSVEntities(request):
    csv_file = request.FILES['entityfilefield']
    io_string = io.StringIO(csv_file.read().decode('UTF-8'))
    reader = csv.reader(io_string, delimiter=',', quotechar='"')
    context = { 'entities': [], 'errors': [] }
    for row in reader:
        name,sortkey,categoryname,url,description = row
        existing = Entity.objects.filter(name=name)
        if existing.exists():
            id = existing.first().id
            if 'showduplicates' in request.POST:
                context['errors'].append(f"Entity named '{name}' already exists (id {id})")
            continue
        if sortkey == '': sortkey = name
        try:
            category = EntityCategory.objects.get(name=categoryname)
        except:
            context['errors'].append(f"No such category '{categoryname}' (in '{name}')")
            continue
        e = Entity(name=name, category=category, sortkey=sortkey, url=url, description=description)
        e.save()
        context['entities'].append(e)
    return render(request, 'importEntitiesResult.html', context)


@login_required
def importCSVLinks(request):
    csv_file = request.FILES['linkfilefield']
    io_string = io.StringIO(csv_file.read().decode('UTF-8'))
    reader = csv.reader(io_string, delimiter=',', quotechar='"')
    context = { 'links': [], 'errors': [] }
    for row in reader:
        name1,linkname,name2 = row
        try:
            entity1 = Entity.objects.get(name=name1)
        except:
            context['errors'].append(f"No such entity '{name1}'")
            continue
        try:
            linkcategory = LinkCategory.objects.get(name=linkname)
        except:
            context['errors'].append(f"No such link category '{linkname}'")
            continue
        try:
            entity2 = Entity.objects.get(name=name2)
        except:
            context['errors'].append(f"No such entity '{name2}'")
            continue
        existing = Link.objects.filter(entity1=entity1, entity2=entity2, category=linkcategory)
        if existing.exists():
            if 'showduplicates' in request.POST:
                context['errors'].append(f"Link {name1}/{linkname}/{name2} already exists")
            continue
        l = Link(entity1=entity1, entity2=entity2, category=linkcategory)
        l.save()
        context['links'].append(l)
    return render(request, 'importLinksResult.html', context)


@login_required
def exportCSVEntities(request):
    entities = Entity.objects.all().order_by('category','sortkey')
    response = HttpResponse(content_type='text/csv', headers={'Content-Disposition': 'attachment; filename="entities.csv"'})
    writer = csv.writer(response, delimiter=',', quotechar='"')
    for e in entities:
        row = [e.name, e.sortkey, e.category.name, e.url, e.description]
        writer.writerow(row)
    return response


@login_required
def exportCSVLinks(request):
    links = Link.objects.all().order_by('entity1','category')
    response = HttpResponse(content_type='text/csv', headers={'Content-Disposition': 'attachment; filename="links.csv"'})
    writer = csv.writer(response, delimiter=',', quotechar='"')
    for l in links:
        row = [l.entity1.name, l.category.name, l.entity2.name]
        writer.writerow(row)
    return response


