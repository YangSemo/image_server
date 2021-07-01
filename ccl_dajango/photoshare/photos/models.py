from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Place(models.Model):
    class Meta:
        # 모델 객체의 이름을 관리자 화면으로 표시
        verbose_name = 'Place'
        # 복수형으로 표시(한국어 설정 시 따로 설정 안해도 됨)
        verbose_name_plural = 'Places'
        # 모델의 정렬 순서 지정
        # ordering = ['name', '-user'] 오름차순, 내림차순 정렬

    name = models.CharField(max_length=100, null=False, blank=False) # 장소명

    def __str__(self):
        return self.name

class Symptom(models.Model):
    class Meta:
        # 모델 객체의 이름을 관리자 화면으로 표시
        verbose_name = 'Symptom'
        # 복수형으로 표시(한국어 설정 시 따로 설정 안해도 됨)
        verbose_name_plural = 'Symptoms'
        # 모델의 정렬 순서 지정
        # ordering = ['name', '-user'] 오름차순, 내림차순 정렬

    name = models.CharField(max_length=100, null=False, blank=False) # 증상명

    def __str__(self):
        return self.name

class File_Info(models.Model):
    class Meta:
        verbose_name = 'File_Info'
        verbose_name_plural = 'File_Infos'

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)  # 사용자
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True) # 장소
    place_detail = models.TextField() # 장소 상세
    symptom = models.ForeignKey(Symptom, on_delete=models.SET_NULL, null=True, blank=True) # 증상
    description = models.TextField() # 증상 설명
    create_at = models.DateTimeField(auto_now_add=True) # 등록 날짜 자동 부여
    file = models.FileField(null=False, blank=False)  # 파일

    def __str__(self):
        return self.description
