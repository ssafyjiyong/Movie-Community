from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:review_pk>/', views.detail, name='detail'),
    path(
        '<int:review_pk>/comments/create/',
        views.create_comment,
        name='create_comment',
    ),
    path('<int:review_pk>/like/', views.like, name='like'),
    path('<int:review_pk>/comment/<int:comment_pk>/delete/',views.comment_delete, name='comment_delete'),
    path('<int:review_pk>/soncomment/<int:comment_pk>/',views.soncomment_create, name='soncomment_create'),
    path('<int:review_pk>/soncomment/<int:soncomment_pk>/delete/',views.soncomment_delete, name='soncomment_delete'),
]
