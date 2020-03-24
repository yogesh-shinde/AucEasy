from django.urls import path
from Auction import views
urlpatterns = [
    path('auction-details/', views.Auction_Details.as_view()),
    path('current-auction/', views.Current_Auction.as_view()),
    path('upcoming-auction/', views.Upcoming_Auction.as_view()),
    path('product-detail/<int:id>/', views.Product_Details.as_view()),
    path('current-bid/<int:cid>/', views.Current_Bid.as_view()),
    path('add-auction/', views.AddAuction.as_view()),
    path('add-to-auction/<int:pid>/', views.AddToAuctionView.as_view()),
]
