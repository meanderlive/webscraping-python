from django.urls import path,include

from django.urls import path, include

from .views import HomeView, CreateListing, ListingView

urlpatterns = [
    path('list/', HomeView.as_view(), name='home1'),
    path('add-listing', CreateListing.as_view(), name='add_listing'),
    path('listings/<slug:slug>/', ListingView.as_view(), name='listing'),
]