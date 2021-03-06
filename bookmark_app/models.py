from django.db import models
from core import models as core_models
from django.contrib.auth.models import User

class List(models.Model):
    title = models.CharField(max_length=30, help_text="Title of list")
    user = models.ForeignKey(User)

    def __str__(self):
        return self.title

class Section(models.Model):
    title = models.CharField(max_length=30, help_text="Title of section")
    the_list = models.ForeignKey(List, related_name='section')

    def __str__(self):
        return self.title

class Link(models.Model):
    display_text = models.CharField(max_length=30, 
                                    help_text="Text to display for link")
    url = models.URLField()
    notes = models.TextField(max_length=500, blank=True,
                             help_text="Additional notes for link")

    section = models.ForeignKey(Section, related_name='link')

    def __str__(self):
        return self.url