from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout # 있으면 들어있는 정보가 들어오고, 없으면 null값이 들어온다.
from django.contrib.auth.models import User
from .forms import LoginForm, UserForm, FindUsernameForm, ResetPasswordForm

# 사용자 가입 : /common/register/
def common_register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data["username"],
                password = form.cleaned_data["password"],
                email = form.cleaned_data["email"],
                first_name = form.cleaned_data["first_name"],
            )
            user.save()
            messages.success(request, "회원가입이 완료되었습니다.")
            return redirect("common:login")
        else:
            for field_name, error_messages in form.errors.items():
                messages.error(request, f"{form.fields[field_name].label} : {error_messages[0]}")
            return render(request, "common/register.html", {"form" : form})

    form = UserForm()
    return render(request, "common/register.html", {"form": form})

# 사용자 아이디 찾기 : /common/find_username/
def common_find_username(request):
    if request.method == "POST":
        form = FindUsernameForm(request.POST)
        if form.is_valid():
            user = User.objects.filter( 
                #사용자 정보를 usermodels에서 불러와서 filter를 넣어서 first_name,email이랑 받아온게 같은거 첫번째거 하나만 받아와라
                first_name = form.cleaned_data["first_name"],
                email = form.cleaned_data["email"]
            ).first()
            if user is not None:
                return render(request, "common/find_username.html", {"username" : user.username}) # username이 있다면 넘겨준다.
            else:
                messages.error(request, "존재하지 않는 사용자입니다.")
        else:
           for field_name, error_messages in form.errors.items():
                messages.error(request, f"{form.fields[field_name].label} : {error_messages[0]}")

    form = FindUsernameForm()
    return render(request, "common/find_username.html", {"form": form})

# 랜덤 비밀번호 생성
def generate_password():
    import random
    import string
    length = random.randint(8, 20)
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    
# 사용자 비밀번호 초기화 : /common/reset_password/
def common_reset_password(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.filter( 
                first_name = form.cleaned_data["first_name"],
                email = form.cleaned_data["email"],
                username = form.cleaned_data["username"]
            ).first()
            if user is not None:
                password = generate_password()
                user.set_password(password)
                user.save()
                return render(request, "common/reset_password.html", {"password" : password})
            else:
                messages.error(request, "존재하지 않는 사용자입니다.")
        else:
           for field_name, error_messages in form.errors.items():
                messages.error(request, f"{form.fields[field_name].label} : {error_messages[0]}")

    form = ResetPasswordForm()
    return render(request, "common/reset_password.html")


# 사용자 로그인 : /common/login/
def common_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data["username"],
                password = form.cleaned_data["password"],
            ) # 없으면 None
            if user is not None:
                login(request, user)
                return redirect("common:profile")
            else:
                messages.error(request, "아이디 또는 비밀번호가 일치하지 않습니다.")
        else:
            for field_name, error_messages in form.errors.items():
                messages.error(request, f"{form.fields[field_name].label} : {error_messages[0]}")
            return render(request, "common/login.html", {"form" : form})
        
    form = LoginForm()
    return render(request, "common/login.html", {"form": form})


# 사용자 로그아웃 : /common/logout/
def common_logout(request):
    logout(request)
    return render(request, "common/logout.html")

# 사용자 정보 : /common/profile/
def common_profile(request):
    return render(request, "common/profile.html")

# 사용자 정보 수정 : /common/update_profile/
def common_update_profile(request):
    return render(request, "common/update_profile.html")

# 사용자 비밀번호 수정 : /common/update_password/
def common_update_password(request):
    return render(request, "common/update_password.html")

