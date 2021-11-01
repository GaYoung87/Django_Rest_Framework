from django.shortcuts import render, redirect
from .models import Article

# 저장되어있는 Article들을 리스팅하는 페이지
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)


# 사용자의 입력을 받아서 data를 'create'로 전달하는 페이지
def new(request):
    return render(request, 'articles/new.html')


# 'new'에서 받은 data로 Article을 저장하는 페이지
def create(request):

    title = request.GET.get('title')  # new.html의 action은 어디로보내겠다. -> 정보들을 articles/create/에 저장
    content = request.GET.get('content')

    article = Article()
    article.title = title
    article.content = content
    article.save()

    return redirect('/articles/')


def delete(request, article_pk):
    # 특정 article의 pk 값을 받아서 해당 article 삭제
    article = Article.objects.get(pk=article_pk)
    article.delete()

    # 삭제가 완료된 후 index 페이지로 돌려보낸다.
    return redirect('/articles/')


# Variable routing으로 받은 article_pk의 데이터를 수정하는 페이지
# 수정한 데이터를 'update'로 전달한다.
def edit(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {'article': article}
    return render(request, 'articles/edit.html', context)


# 'edit'에서 전달받은 데이터를 반영한다.
def update(request, article_pk):
    
    # 수정완료된 데이터들
    title = request.GET.get('title')
    content = request.GET.get('content')

    # 기존 article
    article = Article.objects.get(pk=article_pk)
    
    # 수정 시작
    article.title = title
    article.content = content
    article.save()

    # 인덱스 페이지로 돌아가!
    return redirect('/articles/')