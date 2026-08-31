from django.shortcuts import render
from to_do_app.models import Movie
from django.http import JsonResponse
# Create your views here.
def movie_list(request):
    movies=Movie.objects.all()
    return JsonResponse({"movie":list(movies.values())})

def movie_detail(request,pk):
    movie=Movie.objects.get(pk=pk)
    data={
        "name":movie.name,
        "description":movie.description,
        "review":movie.review,
        "active":movie.active
    }
    return JsonResponse({"movie":data})
    
