import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Place, File_Info, Symptom
from .form import CustomUserCreationForm

from thumb_gen.worker import Generator # 영상 썸네일
# Create your views here.

# 메인 페이지 view
@login_required(login_url='login')
def gallery(request):
    place = request.GET.get('place')
    if place == None:
        # 포토 DB 전체 가져오기
        file_infos = File_Info.objects.all()
    else:
        # 카테고리에 해당되는 포토만 가져오기
        file_infos = File_Info.objects.filter(category__name=place)

    # 카테고리 DB 전체 내용 가져오기
    places = Place.objects.all()

    # 영상을 이미지로 바꾸기
    # folder = 'C:/Users/SAMSUNG/CCLab_git/image_server/ccl_dajango/photoshare/static'
    # for photo in photos:
    #     if photo.image.url.endswith('.mp4') or photo.image.url.endswith('.mkv'):
    #         app = Generator(os.path.join(folder, photo.image.url), output_path=folder, custom_text=False, font_size=25)
    #         app.run()
    for file_info in file_infos:
        print("file_info: ", file_info.file.url)

    # 딕셔너리 형식으로 카테고리, 포토 변환
    context = {'places': places, 'file_infos': file_infos}
    return render(request, 'photos/gallery.html', context)

# 이미지 상세보기 view
@login_required(login_url='login')
def viewPhoto(request, pk):
    # file_info id 불러오기
    file_info = File_Info.objects.get(id=pk)

    # 이미지(png,jpg 등), 영상(mp4) 확장자 추출
    gubun = file_info.file.url[file_info.file.url.find(".")+1:]

    context = {'file_info':file_info, 'gubun': gubun}
    return render(request, 'photos/photo.html', context)

# 이미지 추가 view
@login_required(login_url='login')
def addPhoto(request):
    # 카테고리 DB 내용 가져오기
    places = Place.objects.all()
    symptoms = Symptom.objects.all()

    # requset가 Post일 때
    if request.method == 'POST':
        data = request.POST # Post 방식의 data 객체
        file = request.FILES.get('file') # 업로드한 이미지 가져오기

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

        # File_Info DB에 데이터 전송
        file_info = File_Info.objects.create(
            user = request.user,
            visited_date = data['visited_date'],
            place = place,
            place_detail = data['place_detail'],
            symptom = symptom,
            description = data['description'],
            file = file,
        )
        # gallery.html로 이동
        return redirect('gallery')

    context = {'places': places, 'symptoms':symptoms}
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