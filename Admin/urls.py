from django.urls import path
from Admin import views


urlpatterns = [
    path('home/', views.AdminDisplay.as_view()),

    path('admin-register/', views.AdminRegistration.as_view()),
    path('admin-login/', views.AdminLogin.as_view()),
    path('admin-update/', views.AdminUpdate.as_view()),

    path('pending-verification/', views.PendingVerification.as_view()),
    path('product-verified/', views.ProductVerified.as_view()),



    path('admin-verifyproduct/<int:id>/', views.VerifyProduct.as_view()),
    path('admin-cancelproduct/<int:id>/', views.CancelProduct.as_view()),

    # Add Product Category, Subcategory
    path('add-category/',views.AddProductCategory.as_view()),
    path('add-subcategory/',views.AddProductSubcategory.as_view()),

    # Add Country, State, City, Area
    path('add-country/',views.AddCountry.as_view()),
    path('add-state/',views.AddState.as_view()),
    path('add-city/',views.AddCity.as_view()),
    path('add-area/',views.AddArea.as_view()),
    path('message/',views.message)

]
