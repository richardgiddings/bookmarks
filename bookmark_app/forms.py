from django import forms
from .models import List, Section, Link

class ListForm(forms.ModelForm):

    class Meta:
        model = List
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class SectionForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class LinkForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = ['display_text', 'url', 'notes']

    def __init__(self, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'