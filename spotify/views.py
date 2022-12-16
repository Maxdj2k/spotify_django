# spotify_signup.py

from django.shortcuts import (
    render,
    redirect ,
    get_object_or_404 
)
from . forms import UserRegistrationForm



def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        username = request.POST.get('username')
        print(username)
        password1 = request.POST.get('password1')
        print(password1)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login_user(request, user)
                return redirect('login')
    else:
        form = UserRegistrationForm()
        return render(request, "spotify_registration.html",{'form':form })
    

# spotify_login.py

from django.shortcuts import (
    render,
    redirect ,
    get_object_or_404 
)

from django.contrib.auth import authenticate 
from django.contrib.auth import login as login_user

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login_user(request, user)
            return redirect('home')
    

    return render(request, 'login.html')

# spotify_logout.py

from django.shortcuts import (
    render,
    redirect ,
    get_object_or_404 
)
from django.contrib.auth import logout as logout_user


def logout(request):
    logout_user(request)
    return redirect('login')

# spotify_create.py

from django.views.generic import CreateView
from . models import SpotMusic 
from django.contrib.auth.mixins import LoginRequiredMixin


class SongCreateView(LoginRequiredMixin, CreateView):
    model = SpotMusic
    template_name = 'song-create.html'
    fields = ['song_author','song_title','song_image','audio']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)


# spotify_home.py 

from django.shortcuts import (
    render,
    redirect ,
    get_object_or_404 
)
from . models import SpotMusic 
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def home(request):
    songs = SpotMusic.objects.all()
    return render(request, 'home.html',{'all':songs})

# playsong.py

from django.shortcuts import (
    render,
    redirect ,
    get_object_or_404 
)
from . models import SpotMusic 


def playSong(request,id):
    obj = SpotMusic.objects.get(id=id)
    return render(request, 'playSong.html',{'song':obj })