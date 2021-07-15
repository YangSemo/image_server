from django.contrib import admin

# Register your models here.
from .models import Place, File_Info,Symptom, File
# 관리자 페이지에 추가

# Photo 클래스를 inline으로 나타낸다
class FileInline(admin.TabularInline):
    model = File

class File_Info_Admin(admin.ModelAdmin):
    # 관리자 페이지에 보여주기
    list_display = ('id','user','place','visited_date','place_detail','symptom','description','create_at')
    # 이 순서대로
    ordering = ('-visited_date',)
    # 검색 가능 => 현재 오류 남
    # search_fields = ('place','symptom')

    # File_Info_Admin 클래스는 해당하는 File 객체를 리스트로 관리하는 한다.
    inlines = [FileInline,]

class File_Admin(admin.ModelAdmin):
    list_display = ('id','file','file_info_id')


admin.site.register(File_Info, File_Info_Admin)
admin.site.register(Place)
admin.site.register(Symptom)
admin.site.register(File,File_Admin)

