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


class ArtistDetailSerializer(ArtistSerializer):
    musics = MusicSerializer(many=True)

    class Meta(ArtistSerializer.Meta):
        fields = ArtistSerializer.Meta.fields + ('musics', )



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('music_id', 'content', )