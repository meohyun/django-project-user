from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(
        max_length = 15, 
        unique = True,
        null = True,
        error_messages = {'unique':'중복된 nickname 입니다.'})
    kakao_id = models.CharField(
        max_length = 20,
        null = True,
        validators = [validate_no_special_characters])
    # override
    username = models.CharField(
        max_length = 25,
        null = True,
        unique = False,
        validators = [validate_no_special_characters])
