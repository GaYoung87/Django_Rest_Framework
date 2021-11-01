from django.db import models

# Create your models here.
class Article(models.Model):
    # id(pk)는 기본적으로 처음 테이블이 생성될 때 자동으로 만들어 진다.
    # id = models.AutoField(primary_key=True)  # 처음 값에는 1, 2, 3, 순서로 들어감

    # CharField에서는 max_length가 필수 인자다.
    title = models.CharField(max_length=20)  # 클래스 변수(DB의 필드)
    content = models.TextField()  # 클래스 변수(DB의 필드)
    created_at = models.DateTimeField(auto_now_add=True)
    