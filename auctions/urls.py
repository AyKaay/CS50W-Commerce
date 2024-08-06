from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("", views.index, name="index"),

    # User management
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search", views.search_category, name="search_category"),
    
    # Listing management
    path("create_listing/", views.create_listing, name="create_listing"),
    path("listing/<int:id>/", views.listing_page, name="listing_page"),
    #path("listing/<int:listing_id>/place_bid/", views.place_bids, name="place_bids"),   # Add initial bid price
    path("listing/list_status_open/<int:id>/", views.listing_is_open, name="listing_is_open"),
    #path("listing/comment/<int:id>/", views.listing_comment, name="listing_comment"),
    
    # Watchlist management
    path("listing/add/<int:id>/", views.add_to_watchlist, name="add_to_watchlist"),
    path("listing/remove/<int:id>/", views.remove_from_watchlist, name="remove_from_watchlist"),
    path('watchlist/', views.view_watchlist, name='view_watchlist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)