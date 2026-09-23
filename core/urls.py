from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("menu/", views.menu, name="menu"),
    path("about/", views.about, name="about"),
    path("awards/", views.awards, name="awards"),
    path("reviews/", views.reviews, name="reviews"),
    path("contact/", views.contact, name="contact"),
    path("reviews/<int:pk>/like/", views.like_review, name="like_review"),
]
