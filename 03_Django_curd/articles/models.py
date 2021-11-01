from django.db import models
from imagekit.processors import Thumbnail
from imagekit.models import ImageSpecField

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20)  # 어떤 field정의할지
    # 문자열은 null=True 넣지 말기 blank만 넣기(=빈문자열 넣기 위해), 다른 field는 blank, null 다 사용 가능
    content = models.TextField(blank=True)  # String 문자열 빈 값 저장은 null이 아니라 '' -> null이 적합하지 않음
    # blank: 데이터 유효성과 관련되어 있다. -> 비어있어도 저장해도 괜찮아.(필수는 아니야~)
    # null: 실제 DB와 관련되어 있다. -> 값이 비어있어도 Null로 두지말고 비어두어라
    # '', Null로 저장할 것인지
    image = models.ImageField(blank=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[Thumbnail(200,200)],
        format='JPEG',
        options={'quality': 90},
    )
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now와 비교!
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    # on_delete=models.CASCADE == 'Article 이 삭제되면 Comment도 함께 삭제'
    # 어떤 게시글에 대한 댓글인지 알려주기위해서!
    # article.comment_set이 자동으로 생성-> 이름을 article.comments로 바꿔주기 위해서
    # related_name == 'Article instance가 comment를 역참조 할 수 있는 이름을 정의'
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')  # 이 article을 참조하겠다
    # 1:N 관계에서 바라보고있던 article(게시글)이 삭제되었다면 그 관련 데이터(댓글)도 삭제해라\
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pk']
        # ex. 사진 데이터는 내용이고, meta data는 파일이름, 찍은 날짜, 크기 등등

    def __str__(self):
        return self.content
