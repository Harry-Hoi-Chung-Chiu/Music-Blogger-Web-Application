from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse, resolve
from musicBlogger.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from models import Songs, Blogs, UserProfile
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers

# Create your views here.
def index(request):
    context_dict = {}
    context_dict['message'] ="this is the index page"
    return render(request, 'musicBlogger/index.html', context=context_dict)

def about(request):
    context_dict = {}
    context_dict['message']="This is the about page"
    return render(request, 'musicBlogger/about.html', context=context_dict)

def styling_function(request, add_to_recent, context_dict):

    if(add_to_recent):
        context_dict["page"] = "musicBlogger:" + resolve(request.path_info).url_name
        recent = request.COOKIES.get("recent")
        if(recent):
            context_dict["recent"] = recent.split(",")

    try:
        username = request.user.username
        user_data = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user_data)
        context_dict["profile_picture"] =  user_profile.picture
    except: #User does not exist
        pass

def login(request):
    context_dict = {}
    styling_function(request, True, context_dict)

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password) # Checks if valid password.
 
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('musicBlogger:index'))
            else:
                return HttpResponse("Your Music Blogger account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    else:
        return render(request, 'musicBlogger/login.html', context=context_dict)


@login_required
def logout(request):
    logout(request)
    return redirect(reverse('musicBlogger:index'))

def search(request):
    context_dict = {}
    context_dict['message'] ="This is the search page"
    return render(request, 'musicBlogger/searchBlog.html', context=context_dict)

def add_blog(request, blog_name_slug):
    context_dict = {}
    context_dict['message'] ="This is the add blog page"
    return render(request, 'musicBlogger/add_blog.html', context=context_dict)

def view_blog(request):
    context_dict = {}
    context_dict['message'] ="This is the view blog page"
    return render(request, 'musicBlogger/viewBlog.html', context=context_dict)

def contact_us(request):
    context_dict = {}
    context_dict['message'] ="This is the contact us page"
    return render(request, 'musicBlogger/contact_us.html', context=context_dict)

def profile(request, profile_id):
    cprofile = get_object_or_404(UserProfile, pk=profile_id)
    return render(request, 'musicBlogger/profile.html', {'profile': profile})



def new_account(request):
    context_dict = {}
    context_dict['message'] ="This is the new account page"
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # Save user form data to database
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'image' in request.FILES:
                profile.picture = request.FILES['image']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form,'profile_form': profile_form,'registered': registered}

    return render(request,'musicBlogger/new_account.html',context=context_dict)




# def search(request):
#     query = request.GET.get('q', '')
#     results_songs = Songs.objects.filter(
#         Q(field1__icontains=query) | Q(field2__icontains=query)
#     )
#     results_profiles = UserProfile.objects.filter(
#         Q(field1__icontains=query) | Q(field2__icontains=query)
#     )
#     results_blogs = Blogs.objects.filter(
#         Q(field1__icontains=query) | Q(field2__icontains=query)
#     )
#     data_songs = serializers.serialize('json', results_songs)
#     data_profiles = serializers.serialize('json', results_profiles)
#     data_blogs = serializers.serialize('json', results_blogs)
#     return JsonResponse({'results_songs': data_songs, 'results_profiles': data_profiles, 'results_blogs': data_blogs}, safe=False)