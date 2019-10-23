# API 서버 제작

## 개념

### 1. get : 행동을 말함  // endpoint : resource를 가리킨다(정확한 표시 필요)

method=GET -> endpoints=/posts: post를 주세요

method=GET -> endpoints=/posts/1: 1번 post를 주세요

method=GET -> endpoints=/posts/1/comments: 1번 post의 모든 댓글을 보여주세요

method=GET -> endpoints=/comments?oistid=1: comment를 주는데 postid가 1번인 post를 주세요

method=GET -> endpoints=/posts?userid=1: userid가 1번인 post를 주세요



### 2. post: 무언가를 생성하겠다

method=POST -> /posts: 하나의 포스트를 생성하겠다



### 3. put, patch: 수정하겠다

method=PUT / method=PATCH -> endpoints=/posts/1: 1번 post를 수정하겠다

  - user정보에서 name만 수정 -> patch: name_field(수정하고자하는 field)만 보내면 ok

    ​											 -> put: name만 수정하더라도 수정할 전체 데이터(모든 field)보내



### 4. delete: 삭제하라

method=DELETE -> endpoints=/posts/1: 1번 post를 삭제하겠다



### JASONPlaceholder

- key와 value형태로 생긴 text다.
- string값으로 바꿔서
- 모든 데이터는 json형태로 전달한다.

```
# text값
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```



## 서버 제작

### 1. 장고시작

``` bash
# 가상환경에서
$ pip list
$ python -m pip install --upgrade pip
$ pip install django
$ django-admin startproject api .
```

### 2.  api 사용을 위한 설치

```bash
$ pip install djangorestframework
# rest: url로 resource 표현하는 -> 장고로 rest를 구현하는 framework
```

### 3. settings.py

```python
INSTALLED_APPS = [
    # Local apps
    'musics',

    # Third party apps
    'rest_framework',
    'drf_yasg',
```

### 4.  API urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('musics.urls')),
    path('admin/', admin.site.urls),
]
```

### 5. music - models.py

```python
from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Artist와 1:N 구조 형성
# artist입장 -> artist.music_set.all() ==> artist.musics.all() by related_name
class Music(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='musics')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


# Music과 1:N 구조 형성
class Comment(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    def __str__(self):
        return f'{self.music.pk}번 음악의 {self.pk}번째 댓글'
```

### 6. music - URLS.py

```python
from django.urls import path
from . import views


app_name = 'musics'

# /api/v1/musics/ => 모든 음악
urlpatterns = [
    path('comments/', views.comment_list, name='comment_list'),
    path('musics/<int:music_pk>/', views.music_detail, name='music_detail'),
    path('artists/', views.artist_list, name='artist_list'),
    path('musics/', views.music_list, name='music_list'),
]
```


### 7. music -  serializers.py

```python
from rest_framework import serializers
from .models import Music, Artist, Comment

# 특정 언어에서 사용되는 언어구조를 다른 언어에서도 사용할 수 있게 바이트로 구성
# 직렬화: 자바 시스템 내부에서 사용되는 Object, 
class MusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ('id', 'title', 'artist_id', )


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ('id', 'name', )


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('music_id', 'content', )
```

### 8. music - views.py

````python
from django.shortcuts import render, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response   # api에 대한 응답을 하도록
from .models import Music, Artist, Comment
from .serializers import MusicSerializer, ArtistSerializer, CommentSerializer


# 음악 여러개 가지고 오는 것
@api_view(['GET'])  # 요청 들어온게 어떤 메서드로 처리될 것인지 설정
def music_list(request):
    # 내가 보여주고 싶은 data를 db에서 꺼낸다. 
    musics = Music.objects.all()
    # 여기서 musics는 파이썬만 알고 있는 쿼리셋임. 다른 언어에서는 해석할 수 없음
    # 키, 밸류로 구성되는 스트링으로 넘겨야 "serializing"(django-rest framework사용): 바이트 형식
    #   -> json으로 만들려면 serializers.py 생성
    # json file -> python file 은 deserialize임

    # 꺼냈으면, 다른 어디에서든 꺼낼 수 있게 함
    serializer = MusicSerializer(musics, many=True)  # if 하나면 -> MusicSerializer(music)

    # json형태로 응답
    return Response(serializer.data)


# 음악 하나 가지고 오는 것
@api_view(['GET'])
def music_detail(request, music_pk):
    music = get_list_or_404(Music, pk=music_pk)
    serializer = MusicSerializer(music)  # 한개의 music이므로 many=True 넣지 않음
    return Response(serializer.data)


@api_view(['GET'])
def artist_list(request):
    artists = Artist.objects.all()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def comment_list(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
````

### 9. drf-yasg 이용하기 (music )

```bash
$ pip install drf-yasg
```

```python

```















