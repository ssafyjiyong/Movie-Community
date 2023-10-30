from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('',views.index, name='index'),
    path('create/',views.create, name='create'),
    path('<int:pk>/',views.detail, name='detail'),
    path('<int:pk>/delete/',views.delete, name='delete'),
    path('<int:pk>/update/',views.update, name='update'),
    path('<int:movie_pk>/comment/',views.comment_create, name='comment_create'),
    path('<int:movie_pk>/soncomment/<int:comment_pk>/',views.soncomment, name='soncomment'),
    path('<int:movie_pk>/comment/<int:comment_pk>/delete/',views.comment_delete, name='comment_delete'),
    path('<int:movie_pk>/soncomment/<int:cocomment_pk>/delete/',views.cocomment_delete, name='cocomment_delete'),
    path('<int:movie_pk>/likes/',views.likes, name='likes'),
]