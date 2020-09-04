from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name="create"),
    path("watchlist_action/<int:listing_id>", views.watchlist_action, name = "watchlist_action"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("categories",views.categories,name="categories"),
    path("listing/<str:category>", views.category_list, name="category_list")



]
