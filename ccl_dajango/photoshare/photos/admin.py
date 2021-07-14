from django.contrib import admin

# Register your models here.
from .models import Place, File_Info,Symptom
# 관리자 페이지에 추가

class File_Info_Admin(admin.ModelAdmin):
    # 관리자 페이지에 보여주기
    list_display = ('user','place','visited_date','place_detail','symptom','description','file','create_at')
    # 이 순서대로
    ordering = ('-visited_date',)
    # 검색 가능 => 현재 오류 남
    # search_fields = ('place','symptom')

admin.site.register(File_Info, File_Info_Admin)
admin.site.register(Place)
admin.site.register(Symptom)
