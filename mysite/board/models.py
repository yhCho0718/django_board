from django.db import models

class Board(models.Model):
    title = models.CharField(verbose_name="제목", max_length=100)
    content = models.TextField(verbose_name="내용")
    password = models.CharField(verbose_name="비밀번호", max_length=20)
    created_by = models.CharField(verbose_name="글쓴이", max_length=20)
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    filename = models.CharField(verbose_name="파일명", max_length=100, null=True, blank=True)
    original_filename = models.CharField(verbose_name="원본파일명", max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = 'board' # 데이터베이스에 저장될 테이블의 이름을 명시적으로 지정
        verbose_name = 'board' # Django Admin에서 이 모델의 이름을 표시할 때 사용할 단수형 이름을 지정
        verbose_name_plural = 'boards' # Django Admin에서 이 모델의 복수형 이름을 지정
        ordering = ['-created_at']

    def __str__(self):
        return self.title