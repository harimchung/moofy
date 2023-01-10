from django.urls import path
from . import views

app_name='movies'
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:movie_pk>/', views.comment, name="comment"),
    path('comment/<int:comment_pk>/', views.comment_update_delete, name="comment_update_delete"),
]