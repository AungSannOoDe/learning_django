from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .permission import AdminOrReadOnly,ReviewOrReadOnly
from rest_framework import viewsets
from to_do_app.api.serailizer import (
    MovieSerializer,
    StreamPlatformSerializer,
    WatchListSerializer,ReviewSerializer
)

from to_do_app.models import Movie, StreamPlatform, WatchList,Review

class ReviewList(generics.ListCreateAPIView):
    permission_classes=[AdminOrReadOnly,IsAuthenticated]
    # queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    def get_queryset(self):
        pk=self.kwargs['pk']
        return  Review.objects.filter(watchlist=pk)
    
# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self,request):
#         queryset=StreamPlatform.objects.all()
#         serializer=StreamPlatformSerializer(queryset,many=True)
#         return Response(serializer.data)
#     def retrieve(self,request,pk=None):
#         queryset=StreamPlatform.objects.all()
#         watchlist=get_object_or_404(queryset,pk=pk)
#         serializer=StreamPlatformSerializer(StreamPlatform)
#         return Response(serializer.data)
class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes=[AdminOrReadOnly]
    queryset=StreamPlatform.objects.all()
    serializer_class=StreamPlatformSerializer
class ReviewCreate(generics.CreateAPIView):
    permission_classes=[ReviewOrReadOnly,IsAuthenticated]
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        review_user=self.request.user
        review_request=Review.objects.filter(watchlist=movie,review_user=review_user)
        if review_request.exists():
            return ValidationError("You have already reviewed this movie!")
        if movie.number_rating==0:
            movie.average_rating=serializer.validated_data['rating']
        else :
            movie.average_rating=(movie.average_rating+serializer.validated_data['rating'])/2
        movie.number_rating=movie.number_rating+1
        movie.save()
        serializer.save(watchlist=movie,review_user=review_user)
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[ReviewOrReadOnly,IsAuthenticated]
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
class MovieView(APIView):
    permission_classes=[AdminOrReadOnly]

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieViewDetail(APIView):
    permission_classes=[AdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response(
                {"error": "Movie does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response(
                {"error": "Movie does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            movie.delete()
            return Response(
                {"message": "Deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Movie.DoesNotExist:
            return Response(
                {"error": "Movie does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class WatchViewList(APIView):
    permission_classes=[AdminOrReadOnly]

    def get(self, request):
        watchlist = WatchList.objects.all()
        serializer = WatchListSerializer(watchlist, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetailView(APIView):
    permission_classes=[AdminOrReadOnly]

    def get(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(watchlist)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except WatchList.DoesNotExist:
            return Response(
                {"error": "Watch item does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(
                {"error": "Watch item does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = WatchListSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
            watchlist.delete()
            return Response(
                {"message": "Deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except WatchList.DoesNotExist:
            return Response(
                {"error": "Watch list item does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class StreamViewList(APIView):
    permission_classes=[AdminOrReadOnly]

    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True,context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamDetailView(APIView):

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(platform)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StreamPlatform.DoesNotExist:
            return Response(
                {"error": "Stream platform does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(
                {"error": "Stream platform does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            platform.delete()
            return Response(
                {"message": "Deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except StreamPlatform.DoesNotExist:
            return Response(
                {"error": "Stream platform does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )