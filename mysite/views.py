from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator, ValidationError
from django.views.decorators.cache import never_cache
import smtplib, re

from mysite.forms import DeveloperForm,ProjectForm,BugForm,PostForm,ContactForm,MyUserForm

from mysite.models import developer,user,project,bug,post,company,contact,vote

# Create your views here.


@never_cache
def index(request):
    if request.user.is_authenticated:
        userId = User.objects.get(id=request.user.id)

        try:
            devProfile = developer.objects.get(auth_id=request.user.id)
        except developer.DoesNotExist:
            try:
                userProfile = user.objects.get(auth_id=request.user.id)
            except user.DoesNotExist:
                return render(request, 'mysite/index.html', {'user':request.user})
        return render(request, 'mysite/index.html', {'user':request.user, 'profileFilledAck':request.user})
    else:
        return render(request, 'mysite/index.html')

@never_cache
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('mysite:index'))

@never_cache
def login_(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('mysite:index'))
    try:
        log_in = request.POST['login']
    except MultiValueDictKeyError:
        return render(request, 'mysite/login.html')
    try:
        username = request.POST['username']
        password = request.POST['password']
    except MultiValueDictKeyError:
        error_message = "Missing Credentials"
        return render(request, 'mysite/login.html', {'error_message':error_message})
    user = authenticate(request, username=username,password=password)
    if user is not None:
        login(request, user)
        if not testProfile(user.id):
            return HttpResponseRedirect(reverse('mysite:profileSelection'))
        else:
            return HttpResponseRedirect(reverse('mysite:index'))
    else:
        error_message = "Wrong Credentials"
        return render(request, 'mysite/login.html', {'error_message':error_message})



@never_cache
def register(request):

    errors = []
    #Check if the registeration button has been clicked
    try:
        new_registration = request.POST['register']
    except MultiValueDictKeyError:
        return render(request, 'registration/register.html')

    try:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password_1']
        confirm_password = request.POST['password_2']
    except MultiValueDictKeyError:
        errors.append("Missing elements in form.")

    if len(errors)==0:
        if password!=confirm_password:
            return render(request, 'registration/register.html', {'passwordError':'Passwords dont match'})
        else:
            validateEmail = EmailValidator()
            try:
                validateEmail(email)
                #validate_myEmail(email)
            except ValidationError:
                return render(request, 'registration/register.html', {'emailError':'Invalid Email'})
            registered = register_user(username,email,password)
            #try to register user




    if len(errors)==0 and registered=='success':
            return HttpResponseRedirect(reverse('mysite:login'))
    else:
        return render(request, 'registration/register.html', {'error_message':errors})



def register_user(usr,mail,passcode):

    print("Trying to register user")
    try:
        test_username = User.objects.get(username=usr)
    except User.DoesNotExist:
        user = User.objects.create_user(usr, mail, passcode)
        user.save()
        return "success"

    return "Username is already registered"

@never_cache
def projectListings(request):

    projects = project.objects.all()
    companies  = company.objects.all()
    #print("here the COmp",companies)
    noIssueProject = {}
    nameProject = {}
    for projectVar in projects:
        noIssueProject[projectVar.project_id] = len(bug.objects.filter(project=projectVar,bug_status='L'))
        nameProject[projectVar.project_id] = projectVar.project_name

    return render(request, 'mysite/project_list.html', {'projects':projects,'cardinal': noIssueProject, 'companies':companies })

@never_cache
def project_listings(request,companyId):

    companies  = company.objects.all()
    projects = project.objects.filter(company__companyId=companyId)
    noIssueProject = {}
    nameProject = {}
    for projectVar in projects:
        noIssueProject[projectVar.project_id] = len(bug.objects.filter(project=projectVar))
        nameProject[projectVar.project_id] = projectVar.project_name

    return render(request, 'mysite/project_list.html', {'projects':projects,'cardinal': noIssueProject, 'companies':companies })

@never_cache
def profile_selection(request):
    if testProfile(request.user.id):
        return HttpResponseRedirect(reverse('mysite:index'))
        
    return render(request,'mysite/profileSelection.html',{'user':user})


@never_cache
def profile_fill(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('mysite:index'))
    if testProfile(request.user.id):
        return HttpResponseRedirect(reverse('mysite:index'))

    builtuserVar = User.objects.get(username=request.user.username)
    builtuserVar.is_staff = True
    builtuserVar.save()
    #print(request.user.username," Is user staff ",request.user.is_staff)
    #if not request.user.is_staff:
    #    return HttpResponseRedirect(reverse('mysite:profileUser'))

    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = DeveloperForm(request.POST,request.FILES)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            developerVar = form.save(commit=False)
            developerVar.auth_id = request.user.id
            developerVar.username = request.user.username
            developerVar.email = request.user.email
            developerVar.save()
            #form.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('mysite:showProfile',kwargs={'profileId':request.user.id}))
    # If this is a GET (or any other method) create the default form.
    else:
        form = DeveloperForm()
    return render(request, 'mysite/developers.html', {'form':form})

@never_cache
def show_profile(request,profileId):
    if not testProfile(request.user.id):
        return HttpResponseRedirect(reverse('mysite:404'))

    try:
        devProfile = developer.objects.get(auth_id=profileId)
        devProfile.rating = calcRating(profileId)
        devProfile.save()
    except developer.DoesNotExist:
        try:
            userProfile = user.objects.get(auth_id=profileId)
            userProfile.rating = calcRating(profileId)
            userProfile.save()
        except user.DoesNotExist:
            print("User Not Found")
            return HttpResponseRedirect(reverse('mysite:404'))
        return render(request, 'mysite/profile.html',{'user':request.user,'developer':userProfile})
    return render(request, 'mysite/profile.html',{'user':request.user,'developer':devProfile})

@never_cache
def newProjectLandingPage(request):

    if not testProfile(request.user.id):
        return HttpResponseRedirect(reverse('mysite:index'))

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('mysite:401'))

    userVar = developer.objects.get(auth_id = request.user.id)
    if request.method == 'POST':

        form = ProjectForm(request.POST)
        if form.is_valid():
            ProjectName = form.cleaned_data['project_name']
            ProjectStartDate = form.cleaned_data['start_date']
            ProjectCompany = userVar.company

            ProjectVar = project.objects.create(project_name=ProjectName,start_date=ProjectStartDate,company=ProjectCompany)
            ProjectVar.save()
            #ProjectVar = form.save(commit=False)
            # Make edits
            #ProjectVar.save()

            return HttpResponseRedirect(reverse('mysite:projects'))
    else:
        form = ProjectForm()

    return render(request, 'projects/landing.html', {'form':form})


# Individual Projects page to see issues already registered and also a form to create a new Issue
@never_cache
def projectDisplay(request,projectId):

    if not testProfile(request.user.id):
        return HttpResponseRedirect(reverse('mysite:index'))

    projectVar = project.objects.get(project_id=projectId)
    issuesVar = bug.objects.filter(project__project_id=projectId)
    liveIssuesVar = bug.objects.filter(project__project_id=projectId,bug_status='L')

    if request.method == 'POST':
        form = BugForm(request.POST)
        if form.is_valid():
            bugTitle = form.cleaned_data['bug_title']
            bugDescription = form.cleaned_data['bugDescription']
            projectAssociation = project.objects.get(project_id = projectId)
            bugStatus = 'L'
            userVar = developer.objects.get(auth_id = request.user.id)
            bugVar = bug.objects.create(bug_title=bugTitle, bugDescription=bugDescription, project=projectAssociation, bug_status=bugStatus, bugAssociation=userVar)
            bugVar.save()

            return HttpResponseRedirect(reverse('mysite:projectDisplay',kwargs={'projectId':projectId} ))

    else:
        form = BugForm()

    return render( request, 'mysite/projectPage.html', {'form':form, 'project':projectVar, 'issues':issuesVar,'numberOfIssues':len(liveIssuesVar)})

@never_cache
def issueDisplay(request,projectId,bugId):

    if not testProfile(request.user.id):
        return HttpResponseRedirect(reverse('mysite:index'))

    projectVar = project.objects.get(project_id=projectId)
    issueVar = bug.objects.get(bug_id=bugId)
    devVar = issueVar.bugAssociation
    postVar = post.objects.filter(bug__bug_id=bugId)
    companyId = project.objects.values_list('company',flat=True).filter(project_id=projectId)
    companyVar = company.objects.get(companyId=companyId[0])

    print("Created by : ",devVar)
    print("username : ",devVar.username)

    if request.method == 'POST':
        if issueVar.bug_status == 'R':
            return HttpResponseRedirect(reverse('mysite:issueDisplay', kwargs={'projectId':projectVar.project_id, 'bugId':issueVar.bug_id}))
        form = PostForm(request.POST)
        if form.is_valid():
            postTitle = form.cleaned_data['postTitle']
            postContent = form.cleaned_data['content']
            bugAssociation = issueVar
            userAssociation = developer.objects.get(auth_id = request.user.id)

            postVar = post.objects.create(postTitle=postTitle,content=postContent,bug=bugAssociation,user=userAssociation)
            postVar.save()

            return HttpResponseRedirect(reverse('mysite:issueDisplay', kwargs={'projectId':projectVar.project_id, 'bugId':issueVar.bug_id}))

    else:
            form = PostForm()
    #return HttpResponse(bugId)
    return render(request, 'mysite/issue.html', {'form':form, 'company':companyVar, 'project':projectVar, 'issue':issueVar, 'posts':postVar,'postedBy':devVar})


@never_cache
def E401(request):
    return render(request, 'mysite/401.html')

@never_cache
def contact(request):

    if request.method == 'POST':
         form  = ContactForm(request.POST)
         if form.is_valid():
             contactVar = form.save(commit=False)
             contactVar.save()
             return HttpResponseRedirect(reverse('mysite:contact'))

             #return HttpResponse("Successfully saved record")
    else:
        form = ContactForm()

    return render(request, 'mysite/contact.html',{'form':form})



@never_cache
def E404(request):
    response = render_to_response("404.html")
    response.status_code = 404
    return render(request,'404.html')


@never_cache
def profile_fill_user(request):


    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('mysite:401'))


    if testProfile(request.user.id):
        return HttpResponseRedirect(reverse('mysite:index'))

    print("User Set to user")
    builtuserVar = User.objects.get(username=request.user.username)
    builtuserVar.is_staff = False
    builtuserVar.save()

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = MyUserForm(request.POST,request.FILES)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            userVar = form.save(commit=False)
            userVar.auth_id = request.user.id
            #userVar.username = request.user.username
            #developerVar.email = request.user.email
            userVar.save()

            developerVar = developer(first_name=userVar.name,last_name="",company=company.objects.get(companyName="Buggie"),profile="US",auth_id=userVar.auth_id,email=userVar.email,username=userVar.name,image=userVar.image,profileAuth="U")
            developerVar.save()
            #form.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('mysite:showProfile',kwargs={'profileId':request.user.id}))
    # If this is a GET (or any other method) create the default form.
    else:
        form = MyUserForm()
    return render(request, 'mysite/developersUser.html', {'form':form})

@never_cache
def myIssues(request,devId):
    if not testProfile(request.user.id):
        return HttpResponseRedirect(reverse('mysite:profile'))

    issuesVar = bug.objects.filter(bugAssociation__auth_id=devId)
    developerVar = developer.objects.get(auth_id=devId)
    return render(request, 'mysite/myissues.html',{'issues':issuesVar,'developer':developerVar})



def testProfile(id):
    # False when profile is not filled
    try:
        devProfile = developer.objects.get(auth_id=id)
    except developer.DoesNotExist:
        try:
            userProfile = user.objects.get(auth_id=id)
        except user.DoesNotExist:
            return False

    return True

@never_cache
def castVote(request, postId, userId, voteType):

    postVar = post.objects.get(postId=postId)
    userVar = developer.objects.get(auth_id=userId)
    if voteType == 1:
        voteVar = 'U'
    else:
        voteVar = 'D'

    try:
        myvoteVar = vote.objects.get(postA=postVar,userA=userVar,voteType=voteVar)
        #print(myvoteVar)
        #print("Vote Already Exists")
        return HttpResponseRedirect(reverse('mysite:issueDisplay',kwargs={'projectId':postVar.bug.project.project_id,'bugId':postVar.bug.bug_id}))
    except vote.DoesNotExist:
        if(voteType==1):
            postVar.upvotes += 1
        else:
            postVar.downvotes +=1

        postVar.save()
        voteVar = vote(postA=postVar, userA=userVar, voteType=voteVar)
        voteVar.save()
        return HttpResponseRedirect(reverse('mysite:issueDisplay',kwargs={'projectId':postVar.bug.project.project_id,'bugId':postVar.bug.bug_id}))



    return HttpResponse("success")

@never_cache
def sendEmails(recepients,message):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("rvceise16@gmail.com", "1rv16isxxx")
    for recepient in recepients:
        server.sendmail("rvceise16@gmail.com", recepient, message)
    server.quit()


@never_cache
def resolveIssue(request, bugId):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('mysite:401'))


    bugVar = bug.objects.get(bug_id=bugId)
    userVar = developer.objects.get(auth_id=request.user.id)


    print(bugVar," being deleted by ",userVar)
    if not userVar.auth_id == bugVar.bugAssociation.auth_id:
        return HttpResponseRedirect(reverse('mysite:401'))

    if bugVar.bug_status == 'R':
        bugVar.bug_status = 'L'
    elif bugVar.bug_status == 'L':
        bugVar.bug_status = 'R'

    bugVar.save()

    return HttpResponseRedirect(reverse('mysite:myIssue',kwargs={'devId':request.user.id}))


def calcRating(devId):
    return 2.5


    postVar = post.objects.filter(user=userVar)

    upvotes = 0
    downvotes = 0
    for myPost in postVar:
        upvotes += myPost.upvotes
        downvotes += myPost.downvotes

    if (upvotes+downvotes) == 0:
        upvotes = 1

    return 5*(upvotes/(downvotes+upvotes))
