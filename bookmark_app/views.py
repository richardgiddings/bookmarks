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

    subject = request.GET.get('subject')

    links = Link.objects.filter(subject=subject)
    links = links.order_by('display_text')

    return render(request, template_name='links.html', context={'links': links})