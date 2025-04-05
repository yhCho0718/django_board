from django import forms
from .models import Board
from tinymce.widgets import TinyMCE

# 등록 폼
class BoardForm(forms.ModelForm):
    class Meta:
        model = Board # models.py에서의 class이름
        fields = ["title", "content", "password", "created_by"] # 필드에는 필수적으로 사용자가 넣어야 될 내용만 들어간다.
        widgets = {'test': TinyMCE(attrs={'cols': 80, 'rows': 30})}
        
    def clean_title(self): # clean_칼럼명 : 올바른 제목이 들어왔는지 검증한다.
        title = self.cleaned_data.get("title") # self.cleaned_data.get() : 사용자가 적은 내용 받아오기(trim역할-공백제거)
        if not title:
            raise forms.ValidationError("제목을 입력하세요.") # validationError는 view쪽에서 사용한다.
        if len(title) < 2 or len(title) > 100: # len : 글자수
            raise forms.ValidationError("제목을 2자이상 100자이하로 입력하세요.")
        return title # 깨끗한 정보를 view쪽으로 넘겨준다.
    
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content:
            raise forms.ValidationError("내용을 입력하세요.")
        return content
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("비밀번호를 입력하세요.")
        if len(password) < 2 or len(password) > 20:
            raise forms.ValidationError("비밀번호를 2자이상 20자이하로 입력하세요.")
        return password
    
    def clean_created_by(self):
        created_by = self.cleaned_data.get("created_by")
        if not created_by:
            raise forms.ValidationError("글쓴이 이름을 입력하세요.")
        if len(created_by) < 2 or len(created_by) > 20:
            raise forms.ValidationError("글쓴이 이름을 2자이상 20자이하로 입력하세요.")
        return created_by
    

# 삭제 폼
class BoardDeleteForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["password"]
        
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("비밀번호를 입력하세요.")
        return password
