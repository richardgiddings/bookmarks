from django.shortcuts import render
from .models import List, Subject, Link
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    lists = List.objects.filter(user=request.user)
    lists = lists.order_by('title')

    return render(request, template_name='home.html', context={'lists': lists})

@login_required
def links(request):

    subject_id = request.GET.get('subject')
    subject = Subject.objects.get(id=subject_id)

    links = Link.objects.filter(subject=subject_id)
    links = links.order_by('display_text')

    return render(request, template_name='links.html', 
                  context={'links': links, 'subject': subject})