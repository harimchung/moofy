from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup),
    path('profile/', views.profile),
    path('profile/<int:user_pk>/', views.profileupdate),
    path('user/<int:user_pk>/', views.user_update_delete),
]