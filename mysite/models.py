from django.db import models
from django.utils import timezone
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator, ValidationError

# Create your models here.
class company(models.Model):
    companyName = models.CharField(max_length=50)
    companyId = models.AutoField(primary_key=True)
    companyLogo = models.ImageField(upload_to='company_logo', blank=True)

    def __str__(self):
        return self.companyName


class project(models.Model):

    def validateDate(date):
        if datetime.date.today() < date:
            raise ValidationError("Date is in the future")

    project_name = models.CharField(max_length=200)
    projectDescription = models.TextField()
    project_id = models.AutoField(primary_key=True)
    start_date = models.DateField(default=datetime.date.today,validators=[validateDate])
    #end_date = models.DateField()
    company = models.ForeignKey(company, on_delete=models.CASCADE, default=None)


    def __str__(self):
        return self.project_name




class developer(models.Model):

    PROFILE_CHOICES = (
        ('SSE' , 'Senior Software Engineer'),
        ('ST'  , 'Software Tester'),
        ('SA'  , 'Software Architect'),
        ('SE'  , 'Software Engineer'),
        ('SD'  , 'Software Developer'),
	('SY'  , 'Software Analyst'),
	('BA'  , 'Business analyst'),
	('TS'  , 'Technical support'),
    ('US'  , 'User'),
    )

    PROFILE_AUTH_OPTIONS =  (
            ('U', 'user'),
            ('D', 'developer'),
    )
    first_name = models.CharField(max_length=30)
    #middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    company = models.ForeignKey(company, on_delete=models.CASCADE)
    profile  = models.CharField(max_length=2,choices=PROFILE_CHOICES)
    #dev_id = models.IntegerField()
    auth_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=30)
    username = models.CharField(max_length=20)
    image = models.ImageField(upload_to='profile_image', blank=True)
    profileAuth = models.CharField(max_length=1,choices=PROFILE_AUTH_OPTIONS)
    def __str__(self):
        return self.first_name



class user(models.Model):

    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30,validators=[EmailValidator])
    phone = models.BigIntegerField(validators=[MinValueValidator(7000000000),MaxValueValidator(9999999999)])
    #rating = models.DecimalField(max_digits=5, decimal_places=2, default="")
    auth_id = models.IntegerField(primary_key=True)
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.name


class bug(models.Model):
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    bug_id = models.AutoField(primary_key=True)
    bug_title = models.CharField(max_length=200)
    bugDescription = models.CharField(max_length=1000)
    BUG_STATUS = (
        ('L' , 'LIVE'),
        ('A' , 'ARCHIVED'),
        ('R' , 'RESOLVED'),
    )
    bug_status = models.CharField(max_length=1,choices=BUG_STATUS)
    bugAssociation = models.ForeignKey(developer,on_delete=models.CASCADE)
    postedOn = models.DateTimeField(default=datetime.datetime.now)
    #userAssociation = models.ForeignKey(developer,on_delete = models.CASCADE)
    def __str__(self):
        return self.bug_title

class post(models.Model):
    bug = models.ForeignKey(bug, on_delete=models.CASCADE)
    postId = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(developer, on_delete=models.CASCADE)
    postTitle = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.bug.project.project_name + ">" + self.bug.bug_title + ">"  + self.postTitle

class contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=30,validators=[EmailValidator(message="Enter Valid email", code=None, whitelist=None)])
    phone = models.BigIntegerField(validators=[MinValueValidator(700000000),MaxValueValidator(9999999999)])
    message = models.TextField()

    def __str__(self):
        return self.name
