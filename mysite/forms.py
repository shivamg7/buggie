from django import forms
from mysite.models import developer,company,project,bug,post,contact,user
from django.forms import widgets


class DeveloperForm(forms.ModelForm):
    class Meta:
        model = developer
        fields = ('first_name', 'last_name', 'company', 'profile','image', )


class ProjectForm(forms.Form):

    project_name = forms.CharField()
    start_date = forms.DateField(widget=widgets.SelectDateWidget(years=[y for y in range(1960,2020)]))
    projectDescription = forms.TextField()


class BugForm(forms.ModelForm):
    class Meta:
        model = bug
        fields = ('bug_title', 'bugDescription' )


class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ('postTitle', 'content')

class ContactForm(forms.ModelForm):
    class Meta:
        model = contact
        fields = ('name','email','phone','message')

class MyUserForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ('name','email','phone','image')
