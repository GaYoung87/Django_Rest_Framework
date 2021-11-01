from django import forms
from .models import Article, Comment # 어느 모델의 form인지 정의할 수 있음.

# form 사용하는 가장 큰 이유: 우리가 하기 힘든것들을 알아서해주기 때문
# model form 작성하기
class ArticleForm(forms.ModelForm):

    class Meta:  # 따로 상속받을 필요없음.
        model = Article
        fields = ['title', 'content', ]  # 모든 필드를 다 가지고오겠다.

class CommentForm(forms.ModelForm):

    class Meta:  # 따로 상속받을 필요없음.
        model = Comment
        fields = ['content']  # 모든 필드를 다 가지고오겠다.
        # fields = ['content'] -> content 필드만 가지고오겠다.
        # 선생님코드 fields = '__all__' -> exclude = ['article', ]
