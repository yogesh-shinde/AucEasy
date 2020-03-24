from django.urls import path
from . import views
urlpatterns = [
    #path('guest/', views.UserGuest.as_view()),
    path('home/', views.Home.as_view()),

    path('user-register/', views.UserRegister.as_view()),
    path('user-login/', views.UserLogin.as_view()),
    path('update-profile/', views.UserUpdate.as_view()),

    path('user-verify/', views.UserDisplayVerify.as_view()),

    path('user-email/', views.change_pass_email),
    path('email/<int:id>/', views.change_pass),

    path('user-aboutus/', views.AboutUsUserGuest.as_view()),

    path('contact-us/', views.ContactUs.as_view()),
    


    path('user-logout/', views.logout_view)
]
