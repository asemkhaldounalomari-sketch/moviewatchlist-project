from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .models import Movie, Watchlist
from django.db import IntegrityError 
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse


def home(request):
    return render(request, 'main_app/home.html')

@login_required
def movie_list(request):
   
    watchlist_items = Watchlist.objects.filter(user=request.user).select_related('movie')
    return render(request, 'main_app/movie_list.html', {'watchlist_items': watchlist_items})

@login_required
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        user_status = request.POST.get('status')
        user_rating = request.POST.get('rating')

        movie, created = Movie.objects.get_or_create(
            title=title, 
            defaults={
                'user': request.user,
                'description': description,
            }
        )

        try:
           
            Watchlist.objects.create( 
                user=request.user,
                movie=movie,
                status=user_status,
                rating=int(user_rating) if user_rating else None
            )
        except IntegrityError:

            pass
           

        return redirect('movie_list')

    return render(request, 'main_app/add_movie.html')

@login_required
def edit_movie(request, movie_id):
   
    watchlist_item = get_object_or_404(
        Watchlist.objects.select_related('movie'),
        movie_id=movie_id,
        user=request.user
    )
    movie = watchlist_item.movie

    if request.method == 'POST':
    
        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.save()
        
        watchlist_item.status = request.POST.get('status')
        rating_value = request.POST.get('rating')
        watchlist_item.rating = int(rating_value) if rating_value else None
        watchlist_item.save()

        return redirect('movie_list')

    context = {
        'movie': movie,
        'watchlist_item': watchlist_item,
    }
    return render(request, 'main_app/edit_movie.html', context)

@login_required
def delete_movie(request, movie_id):
    
    watchlist_item = get_object_or_404(
        Watchlist, 
        movie_id=movie_id, 
        user=request.user
    )
    
    if request.method == 'POST':
        watchlist_item.delete()
        return redirect('movie_list')
    context = {
        'movie': watchlist_item.movie
    }
    return render(request, 'main_app/delete_movie.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('login') 
    else:
        form = UserCreationForm()
        
    return render(request, 'main_app/signup.html', {'form': form})