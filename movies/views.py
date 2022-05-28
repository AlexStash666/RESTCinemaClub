from django.db import models
from django.db.models import Avg
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer)
from .service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    """Вывод списка фильмов"""

    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Movie.objects.filter(draft=False)
            .annotate(
                rating_user=models.Count(
                    'ratings',
                    filter=models.Q(ratings__ip=get_client_ip(self.request)),
                )
            )
            .annotate(middle_star=(Avg("ratings__star")))
        )


class MovieDetailView(generics.RetrieveAPIView):
    """Вывод списка фильмов"""

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму"""

    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга к фильму"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(generics.ListAPIView):
    """Вывод списка актеров"""

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    """Вывод актера или режиссера"""

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
