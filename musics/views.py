from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response   # api에 대한 응답을 하도록
from .models import Music, Artist, Comment
from .serializers import MusicSerializer, ArtistSerializer, CommentSerializer, ArtistDetailSerializer


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
    music = get_object_or_404(Music, pk=music_pk)
    serializer = MusicSerializer(music)  # 한개의 music이므로 many=True 넣지 않음
    return Response(serializer.data)


@api_view(['GET'])
def artist_list(request):
    artists = Artist.objects.all()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    serializer = ArtistDetailSerializer(artist)
    return Response(serializer.data)


@api_view(['GET'])
def comment_list(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
