from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import get_object_or_404

# import models
from .models import Movie,MovieList

from django.contrib.auth.decorators import login_required

# uuid 
import re

# JSON res
from django.http import JsonResponse

# Create your views here.
@login_required(login_url='login')
def index(request):
    movies = Movie.objects.all()

    context = {
       'movies': movies, 
    }
    return render(request, 'index.html')

   
def login(request):
    if request.method == 'POST':
       username = request.post['Username']
       password = request.post['Password']

       user = auth.authenticate(username=username, password=password)
       if user is not None:
          auth.login(request, user)
          return redirect('/')
       else:
          messages.info(request, 'Credentials Invalid')
          return redirect('login')
    return render(request, 'login.html')

def signup(request):
    if request == 'POST':
      # pass
      # collect all details sent
      email = request.POST['email']
      username = request.POST['username']
      password = request.POST['password']
      password2 = request.POST['password2']

      if password == password2:
         if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect ('signup')
         elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('signup')
         else:
            user = User.objects.create_user(username=username,email=email, password=password)
            user.save()
            # log user in
            user_login = auth.authenticate(username=username,password=password)
            auth.login(request, user_login)
            return redirect('/')
      else:
         messages.info(request, 'Password Not Matching')
         return redirect('signup')

    else:

      return render(request, 'signup.html')
    
def movie(request,pk):
    movie_uuid = pk
    movie_details = Movie.objects.get(uu_id=movie_uuid)

    context = {
       'movie_details' : movie_details
    }

    return render(request, 'movie.html',context)

@login_required(login_url='login')
def my_list(request):
   context = {

   }
   return render(request, 'my_list.html', context)
@login_required(login_url='login')
def add_to_list(request):
   if request.method =='POST':
      movie_url_id = request.POST.get('movie_id')
      uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4} -[0-9a-f]{12}'
      match = re.search(uuid_pattern, movie_url_id)
      movie_id = match.group() if match else None

      movie = get_object_or_404(Movie, uu_id = movie_id)
      movie_list, created = MovieList.objects.get_or_create(owner_user=request.user, movie=movie)
      
      if created:
         response_data = {'status':'success','message':'Added'}
      else:
         response_data = {'status': 'info', 'message': 'Movie already exists'}   
      
      return JsonResponse(response_data)
   
   else:
      # return error
     return JsonResponse ({'status': 'error', 'message': 'Invalid response'} ,status=400)  
     

def my_list(request):
   if request.method =='POST':
      pass
   else:
      # return error
      pass



@login_required(login_url='login')
def logout(request):
   auth.logout(request)
   return redirect('login')
       