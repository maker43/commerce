from django.urls import path

from . import views

urlpatterns = [
    path("",                                            views.index,              name="index"),
    path("login",                                       views.login_view,         name="login"),
    path("logout",                                      views.logout_view,        name="logout"),
    path("register",                                    views.register,           name="register"),
    path("create",                                      views.create,             name="create"),
    path("listings/<int:listing_id>",                   views.listing_page,       name="listing_page"),
    path("listings/<int:listing_id>/deactivate",        views.deactivate_listing, name="deactivate_listing"),
    path("watchlist/",                                  views.watchlist_view,     name="watchlist_view"),
    path("listings/<int:listing_id>/comment",           views.comment_view,       name="comment_view"),
    path("listings/categories",                         views.categories_view,    name="categories_view"),
    path("listings/categories/<str:category_name>",     views.category_view,      name="category_view")

]
