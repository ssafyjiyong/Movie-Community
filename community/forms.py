from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        label="글 제목",
        widget=forms.TextInput(attrs={'style': 'width: 385px'}),
    )
    movie_title = forms.CharField(
        label="영화 제목",
        widget=forms.TextInput(attrs={'style': 'width: 370px'}),
    )
    rank = forms.DecimalField(
        label="평점",
        max_value=5,
        min_value=0,
        widget=forms.NumberInput(attrs={"step":0.5})
    )
    content = forms.CharField(
        label="글 내용",
        widget=forms.Textarea,
    )
    class Meta:
        model = Review
        fields = ['title', 'movie_title', 'rank', 'content']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="댓글",
        widget=forms.TextInput(attrs={'style': 'width: 80%'}),
    )
    class Meta:
        model = Comment
        fields = ('content',)


class SonCommentForm(forms.ModelForm):
    content = forms.CharField(
        label="답글",
        widget=forms.TextInput(attrs={'style': 'width: 80%;'}),

    )
    class Meta:
        model = Comment
        fields = ('content',)