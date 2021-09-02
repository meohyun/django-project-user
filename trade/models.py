from trade.validators import validate_no_special_characters,validate_student_number
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        error_messages={"unique":"닉네임이 중복입니다."},)
    
    student_number = models.IntegerField(
        null = True,
        unique= True,
        error_messages={"unique":"학번이 중복입니다."},
        validators=[validate_student_number]
    )

    username = models.CharField(
        max_length= 30,
        null= True,
        unique= False,
        validators=[validate_no_special_characters]
    ) 

    profile_pic = models.ImageField(
        upload_to = 'profile_pics',
        default = 'default_profile_pic.jpg'
    )

    intro = models.CharField(
        max_length = 60,
        blank = True
    )

    like_posts = models.ManyToManyField(
        'Post', blank=True, related_name='like_users'
        )
  
    def __str__(self):
        return self.email


class Post(models.Model):
    class_name = models.CharField(max_length=20, validators=[validate_no_special_characters])
    professor_name = models.CharField(max_length=10,validators=[validate_no_special_characters])
    GRADE_CHOICE =[
        (1,'★'),
        (2,'★★'),
        (3,'★★★'),
        (4,'★★★★'),
        (5,'★★★★★'),
    ]
    grade = models.IntegerField(choices=GRADE_CHOICE,default=None)
    
    content = models.CharField(max_length=50)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE )
    upload_files = models.FileField(upload_to='zokbo')
    like_count = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.class_name



class Comment(models.Model):
    comment = models.CharField(max_length=60)
    dt_commented = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post,on_delete= models.CASCADE)
    author = models.ForeignKey(User,on_delete= models.CASCADE)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-id']
    
    def get_edit_url(self):
        return reverse('comment-update',args=[self.post.pk, self.pk])

    def get_delete_url(self):
        return reverse('comment-delete',args=[self.post.pk, self.pk])
