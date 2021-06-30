from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    class Meta:
        # 모델 객체의 이름을 관리자 화면으로 표시
        verbose_name = 'Category'
        # 복수형으로 표시(한국어 설정 시 따로 설정 안해도 됨)
        verbose_name_plural = 'Categories'
        # 모델의 정렬 순서 지정
        # ordering = ['name', '-user'] 오름차순, 내림차순 정렬

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.description
