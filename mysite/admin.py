from django.contrib import admin

# Register your models here.
from .models import developer,project,bug,post,company
from django.contrib.auth.models import User

@admin.register(developer)
class developerAdmin(admin.ModelAdmin):
    pass

@admin.register(bug)
class bugAdmin(admin.ModelAdmin):
    pass

@admin.register(project)
class projectAdmin(admin.ModelAdmin):
    pass

@admin.register(post)
class postAdmin(admin.ModelAdmin):
    pass

@admin.register(company)
class companyAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass
