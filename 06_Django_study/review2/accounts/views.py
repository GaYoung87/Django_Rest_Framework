from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
# UserCreationForm을 통해 user에 대한 정보 가지고옴
# UserChangeForm : 유저 정보를 수정하기 위한 form
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
# Authentication에 대한 행위를 할 수 있음 import login으로 로그인할 수 있음.
from django.views.decorators.http import require_POST
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, CustomUserCreationForm


# 회원가입 form이 제공되어야함
# get: 처음에 signup 눌렀을 때 
# post: form 작성하고나서 가입하기 누르면 post로 이동

def signup(request):
    if request.user.is_authenticated:  # 인증상태라면
        return redirect('articles:index')
    # request.user.username == base.html에서 user.username
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # 기본모델만 쓸 수 있음 -> 우리가 만든 것 넣어줌
                                               # 사용자가 form안에서 id랑 비밀번호 입력한 것
        if form.is_valid():  # 입력값 확인
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:  # == 'GET'
        form = CustomUserCreationForm
    context = {'form': form}
    # 회원가입 페이지 주세요
    return render(request, 'accounts/form.html', context)


# 세션의 정보를 db로 저장
def login(request):  # from django.contrib.auth import login과 이름이 같다.
    # POST: 로그인 시켜줌
    if request.method == 'POST':
        # 로그인 로직
        form = AuthenticationForm(request, request.POST)  # AuthenticationForm에만 첫번째 인자로 request가 들어간다.
        if form.is_valid():
            auth_login(request, form.get_user())  # 사용자의 정보를 주는 함수: form.get_user()
            next_page = request.POST.get('next')  
            return redirect(next_page or 'articles:index')

    else:  # GET: 로그인 페이지 보여줌
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/form.html', context)


# 로그아웃: sessionid 지우기
# 세션에 대한 데이터 저장공간: 쿠키
# session: user라는 데이터 하나 만들기
def logout(request):  # logout에는 login_required가 필요 없다!
    auth_logout(request)
    return redirect('articles:index')


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('articles:index')


@login_required
# 바뀐 정보만 전송
def update(request):
    # 실제 수정해주세요라는 요청이 들어올 때
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')

    # 수정할 수 있는 페이지를 주세요라는 요청이 들어올 때
    else:
        form = CustomUserChangeForm(instance=request.user)  # 기존의 정보 가지고서 update시켜야함.
    context = {'form': form}
    return render(request, 'accounts/form.html', context)


@login_required
# password는 회원정보 수정에서 할 수 없음 -> 장고가 이렇게 설정해놓음. -> 새로 만들어야함.
# password라는 url을 만들고, view함수도 만들어라 -> 장고가 제공하는 기본
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:update')
    else:
        form = PasswordChangeForm(request.user)  # 사용 방법 다름
    context = {'form': form}
    return render(request, 'accounts/form.html', context)