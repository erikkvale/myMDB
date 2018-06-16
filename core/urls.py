from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path(
        'movies',
        views.MovieList.as_view(),
        name='MovieList'
    ),
    path(
        'movie/<int:pk>',
        views.MovieDetail.as_view(),
        name='MovieDetail'
    ),
    path(
        'movie/<int:movie_id>/vote',
        views.CreateView.as_view(),
        name='CreateVote'
    ),
    path(
        'movie/<int:movie_id>/vote/<int:pk>',
        views.UpdateView.as_view(),
        name='UpdateVote'
    ),
    path(
        'movie/<int:movie_id>/image/upload',
        views.MovieImageUpload.as_view(),
        name='MovieImageUpload'
    ),
    path(
        'move/top',
        views.TopMovies.as_view(),
        name="TopMovies"
    ),
]