"""AcuEasy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
# media
from django.conf.urls.static import static
from django.conf import settings
from Admin import views
from User.views import UserGuest
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',UserGuest.as_view()),
    path('buyer/', include('Buyer.urls')),
    path('seller/', include('Seller.urls')),
    path('reports/', include('Reports.urls')),
    path('admingui/', include('Admin.urls')),
    path('product/', include('Product.urls')),
    path('user/', include('User.urls')),
    path('auction/', include('Auction.urls')),
    path('logout/', auth_view.LogoutView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
