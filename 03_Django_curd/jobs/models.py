from django.db import models

# Create your models here.
class Job(models.Model):
    name = models.CharField(max_length=20)
    past_job = models.TextField()
    profile_image = models.ImageField(blank=True)

    def __str__(self):  # 데이터가 어떻게 생성되는지 보여줌
        return self.name  # ex. <Job (3)>를 <Job 김선재>로 보여줌