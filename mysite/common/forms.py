from django import forms
from django.contrib.auth.models import User

# 등록 폼
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name"]
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("사용자 아이디를 입력하세요.")
        if len(username) < 6 or len(username) > 20:
            raise forms.ValidationError("사용자 아이디를 6자이상 20자이하로 입력하세요.")
        return username
    
    def clean_email(self):
       email = self.cleaned_data.get("email")
       if not email:
           raise forms.ValidationError("이메일을 입력하세요.")
       return email
                    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("비밀번호를 입력하세요.")
        if len(password) < 8 or len(password) > 20:
            raise forms.ValidationError("사용자 비밀번호를 8자이상 20자이하로 입력하세요.")
        return password
      
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError("이름을 입력하세요.")
        return first_name
    

# 로그인 폼
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
            
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("사용자 아이디를 입력하세요.")
        return username
                        
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("비밀번호를 입력하세요.")
        return password
      
# 아이디 찾기 폼
class FindUsernameForm(forms.Form):
    email = forms.CharField()
    first_name = forms.CharField()

    def clean_email(self):
       email = self.cleaned_data.get("email")
       if not email:
           raise forms.ValidationError("이메일을 입력하세요.")
       return email
                    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError("이름을 입력하세요.")
        return first_name

# 비밀번호 초기화 폼
class ResetPasswordForm(forms.Form):
    email = forms.CharField()
    first_name = forms.CharField()
    username = forms.CharField()
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("사용자 아이디를 입력하세요.")
        return username
    
    def clean_email(self):
       email = self.cleaned_data.get("email")
       if not email:
           raise forms.ValidationError("이메일을 입력하세요.")
       return email
                          
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError("이름을 입력하세요.")
        return first_name
