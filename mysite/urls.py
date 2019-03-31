from django.conf.urls import url, include, re_path
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.test import SimpleTestCase, override_settings
from django.conf.urls.static import static


from . import views


app_name = 'mysite'

urlpatterns = [
    path('', views.index, name='index'),

    path('register/', views.register, name='register'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('projects/',views.projectListings,name='projects'),
    path('projectsFiltered/<int:companyId>',views.project_listings,name='projects_filtered'),
    path('profile/',views.profile_fill,name='profile'),
    path('profileUser/',views.profile_fill_user,name='profileUser'),
    path('showprofile/<int:profileId>',views.show_profile,name='showProfile'),
    path('newProject/',views.newProjectLandingPage,name='newProject'),
    path('projectDisplay/<int:projectId>/',views.projectDisplay,name='projectDisplay'),
    path('issueDisplay/<int:projectId>/<int:bugId>/',views.issueDisplay,name='issueDisplay'),
    path('myIssues/<int:devId>/',views.myIssues,name='myIssue'),
    path('401/',views.E401,name='401'),
    path('contact/',views.contact,name='contact'),
    re_path(r'^.*$',views.E404),
]
