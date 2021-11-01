from django.shortcuts import render, redirect, get_object_or_404
    # get_object_or_404: 꺼내는데, 거기에 해당하는데이터 없으면 404status코드 제공까지 알아서해줌
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse  # 응답
from .models import Article, Comment
# from IPython import embed  # 너무 개발용.. -> 시간을 멈춘다
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# render: 해당 페이지를 보여준다.
# redirect: ex. delete하면 article 목록을 보여줄 때, index페이지(/article/)에서 보여줘야함으로 그리로 가달라고 버튼을 누르는 것!
@require_GET
def index(request):
    # embed()  # request에 어떤 정보가 들어있는지 확인
    # Article 모델에 있는 모든 object를 가지고 와서 html을 통해서 페이지에 보여준다.
    articles = Article.objects.all()
    context = {'articles':articles}
    return render(request, 'articles/index.html', context)


@require_GET
def detail(request, article_pk):
    # 사용자가 url에 적어보낸 article_pk를 통해 디테일 페이지를 보여준다.
    # 특정 한개의 article을 꺼내는 방법
    # 방법1.
        # model이용: Article.objects.get(pk=article_pk)  
    # 방법2.
    # article이라는 변수에 값을 가지고오는데, Article이라는 모델에서 pk에 해당하는 정보들만 가지고와라
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comments.all()
    form = CommentForm()
    context = {'article': article, 'comments': comments, 'form': form}
    return render(request, 'articles/detail.html', context)
        # return render(request, 'articles/detail.html', {'article': article})해도 위와 동일
        # 시험에 나올 수 있음!



# get: 사용자는 우리에게 작성할 수 있는 html페이지를 받아감
# post: 우리에게 받은 form(작성하는 페이지)에서 실제로 db에 작성(=아티클을 만들어라.))하겠다는 것

# post: 내가 새로 작성을 했는데, 그걸 생성하는거 = 아티클을 만들어라.
# get: 내가 내용을 작성할건데, 그 작성할수있는 form(페이지)를 보여줘라.


# 로그인이 필요하다고 말하는 것! -> 로그인이 되어있어야만 실행 가능
# 다시 돌아와 -> get요청으로만 사용 가능 ==> @requrie_POST가 안적혀있으면 작성 가능!!!
@login_required  # 위치 설정
                 # 만약 아무것도 하지않으면 기본은 '/accounts/login/'
                 # 만약 로그인관련앱 이름이 accounts가 아니면 -> (login_urls='/users/login/')과 같이 설정해야함
    # 바로 로그인 페이지로 보내줌
    # url을 accounts의 로그인으로 설정 -> django는 accounts에 기본으로 setting되어있음
    # --> /accounts/login/으로 보내줌 (이름을 설정했기때문에)
# 로그인 끝나고나면 다시 create페이지로 보내줌
# http://127.0.0.1:8000/accounts/login/?next=/articles/create/  => 로그인 후, 저 페이지로 보내라
def create(request):
    if request.method == 'POST':
        # Article을 생성해달라고 하는 요청
        # 데이터 거내서 Article 생성
        # 실제적으로 데이터를 생성.
        form = ArticleForm(request.POST)  # 사용자의 데이터를 가지고오겠다.  # title, content
        # embed()  # 잠시 코드멈춰서 shell에 들어갔다가 나오면 다시 코드 진행
                 # 데이터까지 적혀있는 것을 보여줌 
        if form.is_valid():  # 유효하지 않으면 else문가서 context에 가서 다시 rendering
            article = form.save(commit=False)  # 데이터는 저장하는 것  # 바로 db에 저장하지는 않겠다.(commit=False)
            article.user = request.user  # 지금 로그인되어있는 정보를 생성할 article의 user정보로 넣겠다.
            article.save()
            return redirect('articles:detail', article.pk)  # 여기서는 index에서 보여준느게 아니라 새로고침.
                            # 그러고나서, index에 들어가서 index가 보여주는 것!
                            # article.pk: article에서 pk를 꺼낸다
                            # article_pk: url에서에서 사용해서 넘겨지는 pk
    else:
        # GET 요청
        # Article을 생성하기 위한 페이지를 달라고 하는 요청
        # 브라우저에서 생성하고 엔터치면 나오는 페이지 보여줌
        form = ArticleForm()  # 비어있는 form
    context = {'form': form}
    return render(request, 'articles/create.html', context)  
            # templates 안에 있는 articles 폴더에 있는 create로 보내라
                # -> templates/articles/create.html에서 templates가 빠져있다고 생각!

# form: 우리가 정의한대로
# model form: form.save()하면 데이터 따로 뽑아낼 필요없이 form으로 한번에 저장

# create함수와 동일. 그러나 중복되는 부분 줄일 수 있으므로 위와같이 작성
# def create(request):
#     if request.method == 'POST':
#         form = ArticleForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('articles:index')
#         else:
#             context = {'form': form}
#             return render(request, 'articles/create.html', context)
        
#     else: 
#         form = ArticleForm()
#         context = {'form': form}
#         return render(request, 'articles/create.html', context) 


# Article 수정/삭제, Comment 생성/삭제를 사용자 로그인 상태에서만 동작 가능하도록 만든다
# 비로그인 상태에서는 수정, 삭제할 수 없음
@login_required  # get으로만 받는 애들을 데리고올 수 있음
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # post의 목적: 기존의 아티클을 수정한 값을 바꾸줌 

    if article.user == request.user:  # 접속user와 작성user이 같으면
        if request.method == 'POST':
            # form에 request.POST로 들어온 애는 수정할 값
            form = ArticleForm(request.POST, instance=article)  # 기존에 존재하는 data에 추가
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article_pk)
        else:  # GET method
            # 이때 form은 기존 처음에 작성되었던 값
            form = ArticleForm(instance=article)  # 특정 데이터를 넣은 채로 form을 보이겠다.
    else:
        return redirect('articles:detail', article_pk)
    context = {'form': form, 'article_pk': article_pk}
    return render(request, 'articles/update.html', context)
    # get : update를 이제 할 것이다 -> update페이지 여기있어
    # post: 수정하려고 데이터 들고왔구나, 원하는데로 수정해줄께. detail page로 보냄


# @login_required  : get으로 받은 애들만 사용가능!
@require_POST  # post요청 들어왔을 때만 가능!
               # get요청으로 들어오면 사용자가 이상한 방법으로 삭제하려고 한 것이다.
# articles/3/delete 를 직접 입력하면 삭제됨. -> 이를 방지해야함!!!
def delete(request, article_pk):
    if request.user.is_authenticated:
    # article_pk에 맞는 article을 꺼낸다.
    # 삭제한다. (POST, form 사용이유: 우리가 제공하는 방법으로만 삭제하게 만들기 위해!)
        article = get_object_or_404(Article, pk=article_pk)
        if article.user == request.user:
            article.delete()
        else:
            return redirect('articles:detail', article_pk)
    return redirect('articles:index')  # redirect는 get요청만 받는다.


@require_POST
def comment_create(request, article_pk):
    if request.user.is_authenticated:
        form = CommentForm(request.POST)  # 사용자가 넘겨준 데이터
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article_id = article_pk
            comment.user = request.user
            comment.save()
    return redirect('articles:detail', article_pk)


# @require_POST
# def comment_create(request, article_pk):
#     # article 몇번인지 불러오기
#     article = get_object_or_404(Article, pk=article_pk)
#     if request.method == 'POST':
#         # 어떤 내용을 작성했는지, detail에서 input의 이름이 content였기때무에, request.POST.get으로 content항목을 받아온다.
#         content = request.POST.get('content')  # 사용자가 넘겨준 데이터
#         # comment라는 모델에 속하는 comment를 만들자.
#         # Comment(article=article) -> 모델에 있는 변수=지정한 aritcle이다.
#         comment = Comment(article=article)
#         # 지정한 article을 지정햇으니까 거기에 content를 넣겠다.
#         comment.content = content
#         comment.save()
#         # context = {'form': form}
        
#         return redirect('articles:detail', article_pk)



@require_POST
def comment_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
    # article = get_object_or_404(Article, pk=article_pk) 쓸 필요가 없다!
    # why? urls에서 article_pk를 가지고와서 comment_delete(request, article_pk, comment_pk):에서 article_pk에 그대로 가지고옴
    #      detail페이지에 리턴할 때만 필요하므로 그 article_pk를 바로 redirect()안에 넣어줌!
    # 대신 article_pk = comment.article_id넣어줘도 괜찮. -> db보면 article_id있음
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
        return redirect('articles:detail', article_pk)
    else:  # else문 필요없음. 
        return HttpResponse('You are Unauthorized', status=401)
        # sessionid삭제 == 로그아웃 -> comment 삭제하기 누르면 


# # 선생님 코드 -> form 사용
# def detail(request, article_pk):
#     article = get_object_or_404(Article, pk=article_pk)
#     comment_form = CommentForm()
#     comments = Comment.objects.all()
#     context = {
#         'article': article, 
#         'comment_form': comment_form, 
#         'comments': comments
#     }
#     return render(request, 'articles/detail.html', context)


# @require_POST
# def comment_create(request, article_pk):
#     form = CommentForm(request.POST)  # 사용자가 넘겨준 데이터
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.article_id = article_pk
#         form.save()
#     return redirect('article:detail', article_pk)


# def comment_delete(request, article_pk, comment_pk):
#     comment = get_object_or_404(Comment, pk=comment_pk)
#     comment.delete()
#     return redirect('article:detail', article_pk)


def like(request, article_pk):
    user = request.user
    article = get_object_or_404(Article, pk=article_pk)  # 필요한 정보 준비 완료

    if article.liked_users.filter(pk=user.pk).exists():  # 좋아요 목록에 있었으면 제거
    # if user in article.liked_users.all(): 윗 줄은 이 말과 동일! (효율은 윗줄이 좋음)
        # user입장에서 user가 좋아요 누른 article중에서 넘겨받은 article 추가하겠다.
        user.liked_articles.remove(article)
        liked = False
    else:  # 좋아요 목록에 없었으면 추가
        user.liked_articles.add(article)
        liked = True
    context = {'liked': liked, 'count': article.liked_users.count()}
    return JsonResponse(context)


# 사용자가 로그인 했을 때만 가능!
def follow(request, article_pk, user_pk):
    # 로그인 한 유저가 게시글 유저를 follow or unfollow 한다.
    user = request.user  # 로그인 유저
    person = get_object_or_404(get_user_model(), pk=user_pk)  # 게시글 주인

    if user in person.followers.all():  # 이미 팔로워임
        person.followers.remove(user)  # 언팔하겠음
    else:
        person.followers.add(user)  # 팔로우하겠음
    return redirect('articles:detail', article_pk)