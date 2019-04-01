from django import forms
from mysite.models import developer,company,project,bug,post,contact,user
from django.forms import widgets


class DeveloperForm(forms.ModelForm):
    class Meta:
        model = developer
        fields = ('first_name', 'last_name', 'company', 'profile','image', )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = project
        fields = ('project_name','projectDescription','start_date')
        widgets = {
                'start_date':widgets.SelectDateWidget(years=[y for y in range(1960,2020)]),
                'projectDescription': forms.Textarea(
                               attrs={'rows': 10,
                                      'cols': 40,
                                      'style': 'height: 7em;'}),
        }



class BugForm(forms.ModelForm):
    class Meta:
        model = bug
        fields = ('bug_title', 'bugDescription' )
        widgets = {
            'bugDescription': forms.Textarea(
                           attrs={'rows': 10,
                                  'cols': 40,
                                  'style': 'height: 7em;'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ('postTitle', 'content')
        widgets = {
            'content': forms.Textarea(
                           attrs={'rows': 10,
                                  'cols': 40,
                                  'style': 'height: 7em;'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = contact
        fields = ('name','email','phone','message')

class MyUserForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ('name','email','phone','image')
