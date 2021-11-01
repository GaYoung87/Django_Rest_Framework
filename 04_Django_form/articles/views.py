from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm


# 모든 article을 보여주는 페이지
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)


# GET으로 들어오면 생성하는 페이지 rendering
# POST로 들어오면 생성하는 로직 수행
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():  # 입력한 form이 유효한지 확인 가능
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')

            article = Article(title=title, content=content)
            article.save()
            return redirect('articles:index')
        
        # else:   # 사용자가 이상한 값을 입력했을 때 보여줌 -> 이 과정을 안하면 None값이 들어옴.
        #         # 실수로 한두개 이상한 값 입력했더라도 이전 입력했던 것 보여줘서 수정요구.
        #     context = {'form': form}
        #     return render(request, 'articles/create.html')
    else:
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'articles/create.html', context)


def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    context = {'article': article}
    return render(request, 'articles/detail.html', context)
