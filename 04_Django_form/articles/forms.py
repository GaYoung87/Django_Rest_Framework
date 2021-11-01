from django import forms


# 사용자에게 입력받는 field만 작성
class ArticleForm(forms.Form):
    title = forms.CharField(
        max_length=20,
        label='제목',  # 원래 title이었음
        # 구글에서 찾아서 하면 ok
        widget=forms.TextInput(  
            attrs={
                'placeholder': 'Enter the title..',
            }
        )
    )

    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(  
            attrs={
                'placeholder': 'Enter the comment..',
                'rows'=5,
                'cols'=10,
            }
        )
    )
    # id, created_at, updated_at은 자동으로 입력 받음