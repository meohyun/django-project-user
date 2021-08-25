from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Post,Comment

# Register your models here.
admin.site.register(User,UserAdmin)
UserAdmin.fieldsets += (("Custom fields",{"fields":("nickname","student_number",'profile_pic','intro')}),)
admin.site.register(Post)
admin.site.register(Comment)
