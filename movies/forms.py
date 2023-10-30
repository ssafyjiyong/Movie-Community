from django import forms
from .models import Movie, Comment

class MovieForm(forms.ModelForm):
    title = forms.CharField(
        label="영화 제목",
    )
    description = forms.CharField(
        label="영화 내용",
        widget=forms.Textarea,
    )
    image = forms.ImageField(
        label="이미지",
    )

    genre_types = (['코미디', '코미디'],
                   ['로맨스', '로맨스'],
                   ['액션', '액션'],
                   ['느와르', '느와르'],
                   ['SF', 'SF'],
                   ['판타지', '판타지'],
                   ['추리/미스터리', '추리/미스터리'],
                   ['드라마', '드라마'])
    genre = forms.ChoiceField(
        label="장르",
        choices=genre_types
    )

    score = forms.DecimalField(
        label="평점",
        max_value=5,
        min_value=0,
        widget=forms.NumberInput(attrs={"step":0.5})
    )
    class Meta:
        model = Movie
        exclude = ('user','like_user',)

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="댓글",
        widget=forms.TextInput(attrs={'style': 'width: 80%; height: 30px'}),

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