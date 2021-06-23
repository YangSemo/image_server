from django.db import models

# Create your models here.
class UserStatus(models.Model):
    # pk 미설정 시 자동 부여
    user_id = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    now_inOut = models.BooleanField()
    time = models.DateTimeField()

class CheckLog(models.Model):
    name = models.CharField(max_length=20)
    now_inOut = models.BooleanField()
    time = models.DateTimeField()

