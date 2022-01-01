from django.contrib.auth import login
from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path('', views.index, name="home"),
    path('signup', views.signup, name="signup"),
    path('login', views.log_in, name="login"),
    path('logout', views.log_out, name="logout"),
    path('update/<int:user_id>/', views.update, name='update'),
    path('<int:user_id>/', views.profile, name='profile'),
    path('myposts', views.posts, name='myPosts'),
    path('post/<int:post_id>/', views.perticularPost, name='post'),
    path('createpost/<int:user_id>/', views.createpost, name='createPost'),

]