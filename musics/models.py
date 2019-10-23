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