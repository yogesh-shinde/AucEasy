from django.urls import path
from Product import views

urlpatterns = [
    path('display-product/', views.DisplayProduct.as_view()),
    path('add-product/', views.AddProduct.as_view()),
    path('update-product/<int:id>/', views.UpdateProduct.as_view()),
    path('send-product/<int:id>/', views.SendProduct.as_view()),
    path('myproduct/', views.MyProduct.as_view()),
]
