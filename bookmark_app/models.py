from django.db import models
from core import models as core_models

class List(models.Model):
    title = models.CharField(max_length=30, help_text="Title of list")
    user = models.ForeignKey(core_models.Profile)

    def __str__(self):
        return self.title

class Subject(models.Model):
    title = models.CharField(max_length=30, help_text="Title of subject")
    the_list = models.ForeignKey(List)

    def __str__(self):
        return self.title

class Link(models.Model):
    display_text = models.CharField(max_length=30, 
                                    help_text="Text to display for link")
    url = models.URLField()
    notes = models.TextField(max_length=500, blank=True,
                             help_text="Additional notes for link")

    subject = models.ForeignKey(Subject)

    def __str__(self):
        return self.url