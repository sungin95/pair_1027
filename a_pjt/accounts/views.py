from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Profile


@login_required
def index(request):
    users = get_user_model().objects.all()  # 저장된 모든 User를 가져온다.
    context = {
        "users": users,
    }
    return render(request, "accounts/index.html", context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        profile_ = Profile()  # 프로필 생성
        if form.is_valid():
            user = form.save()
            profile_.user = user  # 프로필에 유저 추가
            profile_.save()  # 저장
            auth_login(request, user)
            return redirect("accounts:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.user.is_authenticated:
        return redirect("accounts:index")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get("next") or "accounts:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


def logout(request):
    auth_logout(request)
    return redirect("accounts:login")


@login_required
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/detail.html", context)


def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect("accounts:login")


@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:index")
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context=context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:index")
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/change_password.html", context)


@login_required
def profile(request):
    user_ = request.user
    reviews = user_.review_set.all()
    comments = user_.comment_set.all()
    profile_ = user_.profile_set.all()[0]
    context = {
        "reviews": reviews,
        "comments": comments,
        "profile": profile_,
    }
    return render(request, "accounts/profile.html", context)


def profile_update(request):
    user_ = get_user_model().objects.get(pk=request.user.pk)  # 로그인한 유저 정보
    current_user = user_.profile_set.all()[0]  # 그 유저의 프로필
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=current_user)
    context = {
        "profile_form": form,
    }
    return render(request, "accounts/profile_update.html", context)
