from django.db import models

# 하나의 게시글은 3개의 필드를 가지고있음
class Article(models.Model):
    title = models.CharField(max_length=20)  # max_length : 필수인자
    content = models.TextField()  # 필수인자 없음
    created_at = models.DateTimeField(auto_now_add=True)  # 자동으로 현재시간 추가

# 1. 모델 작성      2. 모델 작성했다고 장고에게 알려줘야함($python manage.py makemigrations)
# 3. $ python manage.py makemigrations