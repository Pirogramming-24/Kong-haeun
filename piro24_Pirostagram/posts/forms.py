from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'content']
        widgets = {
            'content':forms.Textarea(attrs={
                'class':'form-control',
                'rows':3,
                'placeholder':'문구를 입력하세요...'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        content = cleaned_data.get('content')

        if not image and not content:
            raise forms.ValidationError(
                '이미지 또는 내용을 하나 이상 입력해야 합니다.'
            )

        return cleaned_data    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'comment-input',
                'rows': 2,
                'placeholder': '댓글을 입력하세요...',
            }),
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        if not content.strip():
            raise forms.ValidationError("댓글을 입력하세요.")
        return content
