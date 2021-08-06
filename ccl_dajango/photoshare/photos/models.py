from django.db import models
from django.contrib.auth.models import User
# from imagekit.models import ProcessedImageField

# Create your models here.
# from pilkit.processors import ResizeToFill

# 장소
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

# 증상
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

# 파일 종류
class File_Kind(models.Model):
    class Meta:
        # 모델 객체의 이름을 관리자 화면으로 표시
        verbose_name = 'File_Kind'
        # 복수형으로 표시(한국어 설정 시 따로 설정 안해도 됨)
        verbose_name_plural = 'File_Kinds'
        # 모델의 정렬 순서 지정
        # ordering = ['name', '-user'] 오름차순, 내림차순 정렬

    name = models.CharField(max_length=100, null=False, blank=False) # 파일 종류

    def __str__(self):
        return self.name

class File_Info(models.Model):
    class Meta:
        verbose_name = 'File_Info'
        verbose_name_plural = 'File_Infos'

    id = models.AutoField(primary_key=True) # 기본키
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)  # 사용자
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True) # 장소
    place_detail = models.TextField() # 장소 상세
    symptom = models.ForeignKey(Symptom, on_delete=models.SET_NULL, null=True, blank=True) # 증상
    description = models.TextField() # 증상 설명
    create_at = models.DateTimeField(auto_now_add=True) # 등록 날짜 자동 부여
    visited_date = models.DateField(null=False, blank=False) # 방문 날짜
    thumbnail_img = models.ImageField(blank=True, null=True) # 썸네일 이미지

    # File_Info를 참조할 때 보여주는 컬럼
    def __str__(self):
        # Text만 가능
        return self.description

# File_Info를 참조하여 여러 파일 담는 테이블 
class File(models.Model):
    file_info = models.ForeignKey(File_Info, blank=True, null=True, on_delete=models.CASCADE)
    file = models.FileField(null=False, blank=False)  # 파일
    file_kind = models.ForeignKey(File_Kind, on_delete=models.SET_NULL, null=True, blank=True) # 파일 종류 외래키


    # 영상은 아직 저장 고려 안함 => 이미지만 저장
    # file = ProcessedImageField(
    #     processors = [ResizeToFill(100, 80)], # 사이즈 조정
    #     format = 'JPEG',                    # 최종 저장 포맷
    #     options = {'quality': 60},
    #     null=False
    # )
