from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response   # api에 대한 응답을 하도록
from .models import Music, Artist, Comment
from .serializers import MusicSerializer, ArtistSerializer, CommentSerializer, ArtistDetailSerializer


# 음악 여러개 가지고 오는 것
@api_view(['GET'])  # 요청 들어온게 어떤 메서드로 처리될 것인지 설정
def music_list(request):
    # 127.0.0.1:8000 : domain
    # /api/v1/musics/ : endpoint <- urls에 우리가 작성하는 것
    # ?artist_pk=1/ : query parameter <- 더 많은 정보 받게 우리가 지정 
    params = {}
    artist_pk = request.GET.get('artist_pk')

    if artist_pk is not None:
        params['artist_id'] = artist_pk

    # 내가 보여주고 싶은 data를 db에서 꺼낸다. 
    musics = Music.objects.filter(**params)  # 전체를 가지고 오겠다.
    # 여기서 musics는 파이썬만 알고 있는 쿼리셋임. 다른 언어에서는 해석할 수 없음
    # 키, 밸류로 구성되는 스트링으로 넘겨야 "serializing"(django-rest framework사용): 바이트 형식
    #   -> json으로 만들려면 serializers.py 생성
    # json file -> python file 은 deserialize임

    # 꺼냈으면, 다른 어디에서든 꺼낼 수 있게 함
    serializer = MusicSerializer(musics, many=True)  # if 하나면 -> MusicSerializer(music)

    # json형태로 응답
    return Response(serializer.data)


# 음악 하나 가지고 오는 것
@api_view(['GET', 'PUT', 'DELETE'])
def music_detail_update_delete(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)
    if request.method == 'GET':
        serializer = MusicSerializer(music)  # 한개의 music이므로 many=True 넣지 않음
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MusicSerializer(data=request.data, instance=music)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    # if request.method == 'DELETE':
    else:
        music.delete()
        return Response({'message': 'Music has been deleted!'})


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


@api_view(['POST'])
def comments_create(request, music_pk):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):  # 검증에 실패하면 400 Bad request 오류를 발생
                            # raise_exception: valid하지 않으면 예외처리하겠닫는 의미
        serializer.save(music_id=music_pk)  # music_id입력하지 않아도 알아서 저장됨.
    return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
def comments_update_and_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'PUT':
        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    # if request.method == 'DELETE':
    else:
        comment.delete()
        return Response({'message': 'Comment has been deleted!'})
    