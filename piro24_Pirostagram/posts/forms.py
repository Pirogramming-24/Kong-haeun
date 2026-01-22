from django import forms
from .models import Post

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