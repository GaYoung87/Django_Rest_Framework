from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Reservation: 중계표 -> doctor.reservation_set.all() -> 불편
# Manytomany field -> doctor.patients.all()
# class Reservation():
#     pass

# 원래는 기본 제공해주는 user를 사용함
# 원래는 장고가 가지고 있는 user model이 있었지만, 우리가 accounts라는 어플에 User모델을 정의했다
class User(AbstractUser):
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='followings'
    )
    # jason.followings => 공정배 / 공정배.followers => jason

