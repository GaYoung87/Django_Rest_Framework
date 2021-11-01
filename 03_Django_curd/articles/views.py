from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment


# articles의 메인 페이지, article list를 보여줌
def index(request):
    # SELECT * FROM articles
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)



# Variable Routing으로 사용자가 보기를 원하는 페이지 pk를 받아서
# Detail 페이지를 보여준다.
def detail(request, article_pk):
    # SELECT * FROM articles WHERE pk=3
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comments.all()  # 모든 정보 가지고와라
    context = {
        'article': article,
        'comments': comments
        }
    return render(request, 'articles/detail.html', context)



# 입력 페이지 제공
# GET /articles/create/ -> 페이지만 받아 가겠다
# def new(request):
#     return render(request, 'articles/new.html')  # 자기 페이지갈때 쓰는 것이 render



# 데이터를 전달받아서 article 생성
# POST /articles/create -> new와 create를  GET, POST를 통해 돌아가게함
def create(request):

    # 만약 GET요청으로 들어오면 html 페이지 rendering
    if request.method == 'POST':
        # /articles/new의 new.html의 form에서 전달받은 데이터들
        title = request.POST.get('title')  # POST하면 들어올정보
        content = request.POST.get('content')
        image = request.FILES.get('image')
        article = Article(title=title, content=content, image=image)  # 새로운 인스턴스 생성
        article.save()
        
        return redirect('articles:detail', article.pk)  # 다른 페이지에 갈때 쓰는 것이 redirect
        # 이쪽으로 바로 이동해라. -> 이때, index함수로 가게 됨

    # 아니라면(POST일 경우) 사용자 데이터 받아서 article 생성
    else:
        return render(request, 'articles/create.html')
 
       
    

# 사용자로부터 받은 article_pk값에 해당하는 article을 삭제한다.
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles:index')
    else:
        return redirect('articles:detail', article_pk)
 # articles에 url에서 index로 만들었는데, 만약 articles말고 movies 앱이 생겼을 때, 각각 url이 생길텐데, 
 # 다 index로 하면 어느 앱에 있는 index 페이지인지 헷깔림.
 # 그래서 templates에 name space를 지정해준 것처럼 하면 ok


# /articles/5/update/
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # POST /article/update : 실제 Update 로직이 수행
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if image:
            article.image = image
        article.title = title
        article.content = content
        article.save()
        return redirect('articles:detail', article.pk)

    # GET /article/update : Update를 하기 위한 Form을 제공하는 페이지
    else:
        article = get_object_or_404(Article, pk=article_pk)
        context = {'article': article}
        return render(request, 'articles/update.html', context)

    
def comments_create(request, article_pk):
    # article_pk에 해당하는 article에 새로운 comment 생성
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = Comment()

        # 객체를 통째로 넘겨줌. 어떤 article에 대한 comment인지 알려주기 위한 작업
        comment.article = article
        # comment.article_id = article_pk 라고 해도 ok
        # 이 둘의 차이점은 없음!

        comment.content = content
        comment.save()
        
        # 생성한 다음 detail page로 redirect
    return redirect('articles:detail', article.pk)


def comments_delete(request, article_pk, comment_pk):
    # POST요청으로 들어왔다면
    if request.method == 'POST':
    # comment_pk에 해당하는 댓글 삭제
        comment = get_object_or_404(Comment, pk=comment_pk)  # 특정 모델가지고오고 없으면, 404페이지 보여줌
        comment.delete()
    # 댓글 삭제 후, detail 페이지로 돌아감
    return redirect('article:detail', article_pk)
