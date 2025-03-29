
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("artworks", views.artworks, name="artworks"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("upload", views.upload_post, name="upload"),
    path('load/<str:category>', views.load_posts, name='load_posts'),
    path("view/<int:page>", views.view_allposts, name="view_allpost"),
    path('upload_comment/<int:post_id>', views.upload_comment, name='upload_comment'),
    path("get_comment/<int:id>", views.get_comment, name="get_comment"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("fetch_profile_posts/<str:username>", views.fetch_profile_posts, name="fetch_profile_posts"),
    path("like/<int:post_id>", views.like_post, name="like_post"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
