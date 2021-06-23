from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Category, Photo
from .form import CustomUserCreationForm
# Create your views here.

# 메인 페이지 view
@login_required(login_url='login')
def gallery(request):
    category = request.GET.get('category')
    if category == None:
        # 포토 DB 전체 가져오기
        photos = Photo.objects.all()
    else:
        # 카테고리에 해당되는 포토만 가져오기
        photos = Photo.objects.filter(category__name=category)

    # 카테고리 DB 전체 내용 가져오기
    categories = Category.objects.all()
    
    # 딕셔너리 형식으로 카테고리, 포토 변환
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)

# 이미지 상세보기 view
@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo':photo})

# 이미지 추가 view
@login_required(login_url='login')
def addPhoto(request):
    # 카테고리 DB 내용 가져오기
    categories = Category.objects.all()

    # requset가 Post일 때
    if request.method == 'POST':
        data = request.POST # Post 방식의 data 객체
        image = request.FILES.get('image') # 업로드한 이미지 가져오기

        # 카테고리 가져오기
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])

        # 카테고리 가져오거나 생성
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
            
        # 카테고리 미 입력/생성 시
        else:
            category = None
        
        # Photo DB에 데이터 전송
        photo = Photo.objects.create(
            category = category,
            description=data['description'],
            image=image,
        )
        # gallery.html로 이동
        return redirect('gallery')

    context = {'categories': categories}
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