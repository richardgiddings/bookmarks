from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import List, Section, Link
from .forms import ListForm, SectionForm, LinkForm

@login_required
def home(request):
    lists = List.objects.filter(user=request.user)
    lists = lists.order_by('title')
    return render(request, template_name='home.html', 
                  context={'lists': lists})

@login_required
def links(request, section_id):
    section = Section.objects.get(pk=section_id)
    links = Link.objects.filter(section=section_id)
    links = links.order_by('display_text')
    return render(request, template_name='links.html', 
                  context={'links': links, 'section': section})

@login_required
def add_list(request):
    a_list = List(user=request.user)
    form = ListForm(request.POST or None, instance=a_list)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bookmarks:home'))
    return render(request, template_name='modify.html', 
                           context={'form': form, 'title': 'Add list'})

@login_required
def edit_list(request, list_id):
    the_list = List.objects.get(pk=list_id)
    if the_list.user != request.user:
        return HttpResponseRedirect(reverse('bookmarks:home'))

    form = ListForm(request.POST or None, instance=the_list)
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bookmarks:home'))
    return render(request, template_name='modify.html', 
                           context={'form': form, 'title': 'Edit list'})

@login_required
def delete_list(request):
    list_id = request.POST.get('id', '')
    the_list = List.objects.get(pk=list_id)
    the_list.delete()
    return HttpResponseRedirect(reverse('bookmarks:home'))

@login_required
def add_section(request, list_id):
    the_list = List.objects.get(pk=list_id)
    section = Section(the_list=the_list)
    form = SectionForm(request.POST or None, instance=section)
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bookmarks:home'))
    return render(request, template_name='modify.html', 
                           context={'form': form, 'title': 'Add section'})

@login_required
def edit_section(request, section_id):
    section = Section.objects.get(pk=section_id)
    form = SectionForm(request.POST or None, instance=section)
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bookmarks:links', 
                                        kwargs={'section_id':section_id}))
    return render(request, template_name='modify.html', 
                           context={'form': form, 'title': 'Edit section'})

@login_required
def delete_section(request):
    section_id = request.POST.get('id', '')
    section = Section.objects.get(pk=section_id)
    section.delete()
    return HttpResponseRedirect(reverse('bookmarks:home'))

@login_required
def add_link(request, section_id):
    section = Section.objects.get(pk=section_id)
    link = Link(section=section)
    form = LinkForm(request.POST or None, instance=link)
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bookmarks:links', 
                                        kwargs={'section_id':section_id}))
    return render(request, template_name='modify.html', 
                           context={'form': form, 'title': 'Add link'})

@login_required
def edit_link(request, link_id):
    link = Link.objects.get(pk=link_id)
    form = LinkForm(request.POST or None, instance=link)
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bookmarks:links', 
                                        kwargs={'section_id':link.section.id}))
    return render(request, template_name='modify.html', 
                           context={'form': form, 'title': 'Edit link'})

@login_required
def delete_link(request):
    link_id = request.POST.get('id', '')
    link = Link.objects.get(pk=link_id)
    section_id = link.section.id # before deleting
    link.delete()
    return HttpResponseRedirect(reverse('bookmarks:links', 
                                        kwargs={'section_id':section_id}))


