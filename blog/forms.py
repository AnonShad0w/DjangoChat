from django import forms
from django.utils.safestring import mark_safe

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class DeleteForm(forms.Form):
    YES_NO_CHOICES = [
    (True, 'Yes'),
    (False, 'No'),
    ]

    yes_no = forms.ChoiceField(
            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}),
            label='',choices=YES_NO_CHOICES)
    
    
