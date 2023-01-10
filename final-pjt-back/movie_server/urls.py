"""movie_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('accounts/', include('accounts.urls')),
    # api/token/ 으로 요청을 보내면, 서버가 토큰을 발급해 준다.
    # 그러면 우리는 이 발급받은 토큰을 서버에 어떤 요청을 할때
    # 필수적으로 헤더에 포함시켜서 요청을 보내야 서버가 인증을 할수 있게 된다.
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),

]
