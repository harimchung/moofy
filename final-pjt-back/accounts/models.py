from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

class User(AbstractUser):
    
    #validators=[MinLengthValidator(2)] 옵션을 쓰면 최소 2자 이상 쓰지 않으면 에러남
    #null=True를 쓰지 않아서 회원가입시 반드시 입력하게 만든다
    #unique=True를 쓰면 중복을 허용하지 않는다
    nickname = models.CharField(max_length=15,validators=[MinLengthValidator(2)])

    ##null=True를 쓰면 입력하지 않아도 회원가입 가능
    sex = models.CharField(max_length=10,null=True) 
    age = models.CharField(max_length=10,null=True)
    profile = models.JSONField(default=list)
    watched_list = models.JSONField(default=list)
    selectedGenre = models.JSONField(default=list)

