from django.urls import path
from musicBlogger import views

app_name = "musicBlogger"

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about,name='about'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('search_blogs/', views.search_blogs, name='search_blogs'),
    path('new_account/', views.new_account, name='new_account'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('logout/',views.user_logout, name="logout"),
    path('write_blog',views.write_blog,name='write_blog'),
    path('search_users',views.search_users,name='search_users')

]
