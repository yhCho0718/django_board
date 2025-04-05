# 장고를 이용한 게시판 프로젝트

## 앱 개발 순서

1. 앱 생성

2. 모델 생성

models.py

3. 폼 생성

forms.py 

4. 뷰 생성

views.py

5. URL 생성

urls.py

6. settings.py 수정

- INSTALLED_APPS 추가
- URLS 추가

7. 마이그레이션
```shell
python manage.py makemigrations
python manage.py migrate
만들어진 파일을 바탕으로 실제 db에 적용
```

8.