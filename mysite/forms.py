from django import forms
from mysite.models import developer,company,project,bug,post
from django.forms import widgets


class DeveloperForm(forms.ModelForm):
    class Meta:
        model = developer
        fields = ('first_name', 'last_name', 'company', 'profile','email','image', )


class ProjectForm(forms.Form):

    project_name = forms.CharField()
    start_date = forms.DateField(widget=widgets.SelectDateWidget(years=[y for y in range(1990,2019)]))
    


class BugForm(forms.ModelForm):
    class Meta:
        model = bug
        fields = ('bug_title', 'bugDescription' )


class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ('postTitle', 'content')
