from django.db import models
from django.core.validators import EmailValidator, MinValueValidator
from django.conf import settings



# article.liked_users.all() -> 게시글을 좋아요 누른 사람들
# user.liked_articles.all() -> 내가 좋아요 누른 게시글들...
class Article(models.Model):  # model명은 단수로! app 이름은 보통 복수로!
    title = models.CharField(max_length=20)  # max_length: 필수적으로 들어가야함!
    content = models.TextField()  # TextField로 하는 이유: 내용이 길 수 있어서
    created_at = models.DateTimeField(auto_now_add=True)  # 날짜와 시간 동시저장
    updated_at = models.DateTimeField(auto_now=True)
    # article.user -> article을 작성한 user정보를 바로 가지고 올 수 있다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 한명의 유저가 여러개 article생성하는데, 회원탈퇴하면 article을 삭제할 것이다 -> on_delete=models.CASCADE
    # models.py에서는 user model 쓸 때, settings로부터 직접 가지고온다 -> get_user_model()사용하지 않음
    # on_delete=models.CASCADE: 연결되어있는 관계가 끊어지면, 해당 article도 삭제
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles')
                            # article.liked_users.all()  //  related_name -> user.liked_articles.all() 가능 
    class Meta:  # 데이터를 위한 데이터
        ordering = ('-pk', )  # tuple로 인식하도록 ,를 붙인다
        # 새로 만든 애들이 위쪽으로 쌓일 수 있도록

# 모델링 했다고 장고에게 알려주러 간다.
# $ python manage.py makemigrations -> 알려줌(실제 db에 반영시키지 않음)
        # 이때, content내용이 없어도 에러나지 않음
# $ python manage.py migrate -> 실제 db에 넣음

# 이미 만들어져있는 db에 항목 추가하려면 class에 나중에 content 추가해서 넣으려면 
# $ python manage.py makemigrations
# 1
# ''  #실제 db에 반영된 것은 아님
# $ python manage.py migrate  -> 반영


class Person(models.Model):
    name = models.CharField(max_length=10)
    email = models.CharField(
        max_length=100,
        validators=[EmailValidator(message='이메일 형식에 맞지 않습니다.')]
    )
    age = models.IntegerField(
        validators=[MinValueValidator(19, message='미성년자는 노노')]
    )


class Comment(models.Model):
    # article.comment_set.all() -> related_name 하면 article.comments.all()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # comment는 article에 대한 정보 가지고있음 -> comment.article 로 접근 가능
    # related_name='comments' -> article한테 뭐라고불리고싶어? 난 comments라고 불리고 싶어
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')  # 몇번째 article에 대한 comment인지 확인하기위해 필수! -> 1:N의 관계!!
            # on_delete 설정 : 참조한 키가 삭제되면 그 키와 관련된 데이터를 같이 삭제해주세요
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')

    class Meta:  # 데이터를 위한 데이터
        ordering = ('-pk', )  # 1. tuple로 인식하도록 ,를 붙인다
                              # 2. 새로 만든 애들이 위쪽으로 쌓일 수 있도록
