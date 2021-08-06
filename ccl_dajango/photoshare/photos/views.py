from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Place, File_Info, Symptom, File, File_Kind
from .form import CustomUserCreationForm

# from thumb_gen.worker import Generator # 영상 썸네일
# Create your views here.

# 메인 페이지 view
@login_required(login_url='login')
def gallery(request):
    # 방문장소/증상필터링
    place = request.GET.get('place')
    symptom = request.GET.get('symptom')

    if place != None:
        # 카테고리에 해당되는 포토만 가져오기
        file_infos = File_Info.objects.filter(place__name=place).order_by('visited_date')
    elif symptom != None:
        # 카테고리에 해당되는 포토만 가져오기
        file_infos = File_Info.objects.filter(symptom__name=symptom).order_by('visited_date')
        print("symptom: ", file_infos)
    else:
        # 포토 DB 전체 가져오기
        file_infos = File_Info.objects.all().order_by('visited_date')

    # 카테고리 DB 전체 내용 가져오기
    places = Place.objects.all()
    symptoms = Symptom.objects.all()
    file_kinds = File_Kind.objects.all()



    # 카테고리, 파일 딕셔너리 형식으로  생성
    context = {'places': places, 'symptoms':symptoms, 'file_kinds':file_kinds,'file_infos': file_infos}
    return render(request, 'photos/gallery.html', context)

    # 영상을 이미지로 바꾸기
    # folder = 'C:/Users/SAMSUNG/CCLab_git/image_server/ccl_dajango/photoshare/static'
    # for photo in photos:
    #     if photo.image.url.endswith('.mp4') or photo.image.url.endswith('.mkv'):
    #         app = Generator(os.path.join(folder, photo.image.url), output_path=folder, custom_text=False, font_size=25)
    #         app.run()
    # for file_info in file_infos:
    #     print("file_info: ", file_info.file.url)

# 이미지 상세보기 view
@login_required(login_url='login')
def viewPhoto(request, pk):
    # file_info id 불러오기
    file_info = File_Info.objects.get(id=pk)

    # File_Info의 ID를 기준으로 File 테이블의 file 추출을 위함
    files = File.objects.filter(file_info_id=file_info.id)
    print("file_info 이미지: ",file_info.thumbnail_img.url)

    # gubuns = []  # 확장자를 담기 위함

    # 이미지(png,jpg 등), 영상(mp4) 확장자 추출 => 이미지 영상 구분을 위함
    # for file in files:
    #     gubun = file.file.url[file.file.url.find(".")+1:]
    #     gubuns += gubun

        # photo.html => 이미지, 영상 구분을 위한 코드
        # { % if gubuns[i] == 'mp4' %}
        # < video style = "max-width: 100%; max-height: 100%;" controls loop muted src = "{{files[i].file.url}}" > < / video >
        # {% else %}
        # < img style = "max-width: 100%; max-height: 100%;" src = "{{file.file.url}}" >
        # {% endif %}

        # print('list: ', lists[0][1].file.url)
    # len_gubuns= len(gubuns)

    # context = {'file_info':file_info, 'gubuns': gubuns, 'files': files, 'len_gubuns': len_gubuns}
    context = {'file_info':file_info, 'files': files}
    return render(request, 'photos/photo.html', context)

# 이미지 추가 view
@login_required(login_url='login')
def addPhoto(request):
    # DB 내용 가져오기
    places = Place.objects.all()
    symptoms = Symptom.objects.all()
    file_kinds = File_Kind.objects.all()

    # requset가 Post일 때
    if request.method == 'POST':
        data = request.POST # Post 방식의 data 객체

        # 방문 장소 가져오기
        if data['place'] != 'none':
            place = Place.objects.get(id=data['place'])

        # 증상 가져오기
        if data['symptom'] != 'none':
            symptom = Symptom.objects.get(id=data['symptom'])



        # 카테고리 가져오거나 생성
        # elif data['place_new'] != '':
        #     place, created = Place.objects.get_or_create(name=data['place_new'])

        # 카테고리 미 입력/생성 시
        else:
            place = None
            symptom = None

        # print('첫번째 이미지: ', request.FILES['file'])

        # File_Info DB에 데이터 전송
        File_Info.objects.create(
            user=request.user,
            visited_date=data['visited_date'],
            place=place,
            place_detail=data['place_detail'],
            symptom=symptom,
            description=data['description'],
            thumbnail_img=request.FILES['file'] # 마지막 선택 파일만 썸네일 이미지 저장
        )

        # File_Info의 ID값을 File 테이블 외래키로 사용을 위함 => 최신 등록 id가 제일 크므로 last() 사용
        file_info = File_Info.objects.order_by('id').last()
        # print('file_info ID: ', file_info.id)

        i = 0  # file_names 접근 인덱스

        # name 속성이 file input 태그로부터 받은 파일들을 반복문을 통해 하나씩 가져온다
        for file in request.FILES.getlist('file'):
            # 여러 개의 file_name 가져오기
            file_names = request.POST.getlist('file_name')

            # '파일 종류 미선택 항목 제거"
            for file_name in file_names:
                if file_name=='파일종류 선택':
                    file_names.remove(file_name)

            file_db = File() # File 객체 생성
            file_db.file = file # file 컬럼에 파일 저장

            # 파일 종류 가져오기
            file_name = File_Kind.objects.get(name=file_names[i])
            i += 1  # file_names 배열 인덱스 +1
            file_db.file_kind = file_name

            # print("file_kind: ", file_name)

            file_db.file_info_id = file_info.id # File_Info 외래키
            # print("file: ", file)
            file_db.save() # DB에 저장

        # gallery.html로 이동
        return redirect('gallery')

    context = {'places': places, 'symptoms':symptoms, 'file_kinds' : file_kinds}
    return render(request, 'photos/add.html', context)

# 로그인 view
def loginUser(request):
    page = 'login' # 로그인 페이지에서 인지를 위함
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # user 객체 생성
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) # 로그인 실행
            return redirect('gallery') # gallery 페이지로 이동

    # page 변수 전달
    return render(request,'photos/login_register.html', {'page' : page})

# 로그아웃 view
def logoutUser(request):
    logout(request)
    return redirect('login')

# 회원가입 view
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm() # 회원 가입 form 불러오기

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print('post')
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            print('user: ', user)

            if user is not None:
                login(request,user)
                return redirect('gallery')

        else:
            print('비밀번호를 다시 설정해주세요')


    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)