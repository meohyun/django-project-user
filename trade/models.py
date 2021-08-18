from trade.validators import validate_no_special_characters,validate_student_number
from django.db import models
from django.contrib.auth.models import AbstractUser

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

    def __str__(self):
        return self.email


class Post(models.Model):
    class_name = models.CharField(max_length=20, validators=[validate_no_special_characters])
    professor_name = models.CharField(max_length=10,validators=[validate_no_special_characters])
    GRADE_CHOICE =[
        (1,★),
        (2,★★),
        (3,★★★),
        (4,★★★★),
        (5,★★★★★),
    ]
    grade = models.IntegerField(choices=GRADE_CHOICE)
    upload_files = models.FileField(upload_to='zokbo')
    content = models.TextField()
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User,on_delete=models.CASCADE )

    def __str__(self):
        return self.class_name
