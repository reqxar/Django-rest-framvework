from django.db import models
from django_filters import filterset
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend


from .models import Movie, Actor
from .serializers import (
    CreateRatingSerializer, 
    MovieListSerializer, 
    MovieDetailSerializer, 
    ReviewCreateSerializer,
    ActorListSerializer,
    ActorDetailSerializer
    )
from .service import get_client_ip, MovieFilter



class MovieListView(generics.ListAPIView):
    '''Вывод списка фильмов'''
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    '''Полный вывод фильма'''

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    '''Добавление отзыва к фильму'''

    serializer_class = ReviewCreateSerializer



class AddStarRatingView(generics.CreateAPIView):
    '''Добавление рейтинга к фильму'''

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
        


class ActorListView(generics.ListAPIView):
    '''Вывод списка актеров'''

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    '''Вывод полной информации о человеке'''

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer    
    