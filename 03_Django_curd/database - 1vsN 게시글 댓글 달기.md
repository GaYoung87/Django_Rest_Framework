# database - 1 : N 게시글 댓글 작성

### Article(1개)있으면 그곳에 댓글(여러개)달기

```python
# Article의 models.py
from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20)  # 어떤 field정의할지
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now와 비교!
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    # on_delete=models.CASCADE == Article 이 삭제되면 Comment도 함께 삭제
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  # 이 article을 참조하겠다
    # 1:N 관계에서 바라보고있던 article(게시글)이 삭제되었다면 그 관련 데이터(댓글)도 삭제해라\
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pk']
        # ex. 사진 데이터는 내용이고, meta data는 파일이름, 찍은 날짜, 크기 등등

    def __str__(self):
        return self.content
```

```bash
$ pip install django_extensions  # 다양한 일을해줌
```

```python
# crud settings.py
INSTALLED_APPS = [
    # Local apps
    'articles',
    'jobs',

    # Thrid party apps
    'django_extensions', 
    
    #Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

```bash
$ python manage.py shell_plus
>>> article = Article()
>>> article.title = '새로운 데이터'
>>> article.content = '새로운 내용'
>>> article.save()
>>> article
<Article: Article object (13)>
>>> comment = Comment()
>>> comment.content = 'First comment'
>>> comment.article = article  # comment.article_id = article.pk와 똑같이 동작
							# 누구의 article인지만 
>>> comment.article_id = article.pk  # article의 pk값을 넣겠다.
>>> comment.save()
>>> comment
<Comment: First comment>
>>> comment.article
<Article: Article object (13)>
>>> comment.article_id  # 어디에 달린 댓글인지 알 수 있음
13
>>> comment.article.pk
13
>>> comment.article.content  # article의 새로운 내용
'새로운 내용'
>>> comment.article.title
'새로운 데이터'
>>> comment.pk
1
>>> comment = Comment(article=article, content='Second comment')  # 동시에 새로운 내용 입력
>>> comment.save()
>>> comment.pk
2
>>> comment.content
'Second comment'   # 현재 13번째 article에 2개의 댓글이 달려있음

>>> dir(article)  # 어떤 속성, 어떤 method를 사용할 수 있는지 보여줌

In [1]: article = Article.objects.get(pk=13)

In [2]: article
Out[2]: <Article: Article object (13)>

In [3]: comments = article.comment_set.all()

In [4]: comments
Out[4]: <QuerySet [<Comment: Second comment>, <Comment: First comment>]>
```

```bash
In [1]: article = Article.objects.get(pk=13)

In [2]: article
Out[2]: <Article: Article object (13)>

In [3]: comments = article.comment_set.all()

In [4]: comments
Out[4]: <QuerySet [<Comment: Second comment>, <Comment: First comment>]>
# 특정 article에 달린 댓글 가지고옴. 늦게 달릴수록 앞에 보임.

article.comment_set.filter(content='Second comment').first()  # article에 내가 원하는 댓글 가지고오게하는것
```

```bash
$ python manage.py runserver
# detail 페이지에 댓글 다는 것이 맞다. -> 추가, 삭제 버튼도 만들 수 있음
```



### 댓글 보여주기

```python 
# Detail 페이지를 보여준다.
# url.py 새롭게 불러와 page에 너며줌
def detail(request, article_pk):
    # SELECT * FROM articles WHERE pk=3
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comment_set.all()  # 모든 정보 가지고와라
    context = {
        'article': article,
        'comments': comments
        }
    return render(request, 'articles/detail.html', context)
```

### comments_create함수생성 후 detail 수정

```python
def comments_create(request, article_pk):
    # article_pk에 해당하는 article에 새로운 comment 생성
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = Comment()
        comment.article = article
        # comment.article_id = article_pk
        comment.content = content
        comment.save()
        
        # 생성한 다음 detail page로 redirect
    return redirect('articles:detail', article.pk)
```

```django
{% extends 'base.html' %}

{% block title %}Article Detail{% endblock title %}

{% block body %}
  <h1>{{ article.title }}</h1>
  <p>작성일자: {{ article.created_at }}</p>
  <hr>
  <p>{{ article.content }}</p>
  <hr>
  <h4>Comments</h4>
  {% comment %} 댓글 작성을 위한 form {% endcomment %}
  <form action="{% url 'articles:comments_create' article.pk %}" method="POST">
  {% csrf_token %}
    <input type="text" name="content">
    <button type="submit">댓글 작성</button>
  </form>

  <ul>
  {% for c in comments %}
    <li>{{ c.content }}</li>
  {% empty %}
    <p>아직 댓글이 없습니다.. </p>
  {% endfor %}
  </ul>
  <hr>

  <a href="{% url 'articles:index' %}">[뒤로가기]</a>
  <a href="{% url 'articles:update' article.pk %}">[수정하기]</a>
  <form action="{% url 'articles:delete' article.pk %}" method="POST" onclick="return confirm('Are you sure?')">
  {% csrf_token %}
  <button type="submit">삭제하기</button>
  </form>
{% endblock body %}

```

