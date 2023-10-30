from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.views.decorators.http import require_http_methods, require_POST
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# 로그인 폼 출력
# 유효성 검증 및 세션 데이터 저장 
@require_http_methods(['GET','POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/login.html', context)

# DB와 클라이언트의 쿠키에서 인증된 사용자의 세션 데이터 삭제
@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('movies:index')

# 회원가입 폼 출력
# 유효성 검증 및 회원 데이터 저장 
@require_http_methods(['GET','POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/signup.html', context)

# 단일 회원 데이터 삭제
@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('movies:index')

# 회원정보수정 폼 출력
# 유효성 검증 및 회원 데이터 수정 
@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance = request.user)
    context = {
        'form':form,
    }
    return render(request, 'accounts/update.html', context)

# 비밀번호 변경 폼 출력
# 유효성 검증 및 비밀번호 변경
@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request, user_pk):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form,
    }
    return render(request, 'accounts/change_password.html', context)


@login_required
def profile(request, username):
    user = get_user_model()
    person = user.objects.get(username=username)
    context = {
        'person':person,
    }
    return render(request, 'accounts/profile.html/', context)


@login_required
def follow(reqest, user_pk):
    user = get_user_model()
    you = user.objects.get(pk=user_pk)
    me = reqest.user

    if me != you:
        if me in you.followers.all():
            you.followers.remove(me)
        else:
            you.followers.add(me)
    return redirect('accounts:profile', you.username)


@login_required
def following(request, user_pk):
    user = get_user_model()
    person = user.objects.get(pk=user_pk)
    context = {
        'person':person
    }
    return render(request, 'accounts/following.html/', context)


@login_required
def follower(request, user_pk):
    user = get_user_model()
    person = user.objects.get(pk=user_pk)
    context = {
        'person':person,
    }
    return render(request, 'accounts/follower.html/', context)