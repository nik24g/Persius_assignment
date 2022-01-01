from django.http.request import validate_host
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Post, Comment
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def index(request, *args, **kwargs):
    if request.user.is_anonymous:
        return redirect("/login")
    context = {}
    posts = Post.objects.all()
    context['posts'] = posts
    if request.method == "POST":
        commentDsc = request.POST.get('comment')
        postId = request.POST.get('post')
        commentUser = request.user
        try:
            post = Post.objects.get(pk=postId)
        except Post.DoesNotExist:
            return HttpResponse('Post does not exists')
        comment = Comment(post=post, comment_user=commentUser, comment=commentDsc)
        comment.save()
    return render(request, 'index.html', context)


def signup(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        age = request.POST['age']
        address = request.POST.get('address')
        image = request.FILES.get('image')
        password = request.POST['password']
        re_password = request.POST['re_password']

        # check for errorneous inputs
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return render(request, 'signup.html')
        if password != re_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')
        if int(age) < 12:
            messages.error(request, "Age must be greater than 12")
            return render(request, 'signup.html')

        # creat user
        new_user = User.objects.create_user(username, email, password, first_name=firstname, last_name=lastname, age=age, address=address, image=image)

        new_user.save()
        messages.success(request, 'Your account has been successfully created Please Login.')
    return render(request, 'signup.html')


def log_in(request):
    if request.method == "POST":
        # check that user login with correct credentials
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')


def log_out(request):
    logout(request)
    return redirect("/login")

def profile(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get("user_id")

    if request.user.is_authenticated:
        try:
            account = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse("user not found")

        # check that user is looking for own profile or not 
        if account == request.user:
            context['id'] = account.id
            context['username'] = account.username
            context['first_name'] = account.first_name
            context['last_name'] = account.last_name
            context['age'] = account.age
            context['email'] = account.email
            context['address'] = account.address
            context['image'] = account.image.url
            return render(request, 'profile.html', context)
        else:
            return HttpResponse("You can not see others profile.")
    else:
        return redirect("/login")

def update(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("/login")
    user_id = kwargs.get("user_id")
    try:
        account = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponse("Something went wrong")
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile")
    context = {}

    if request.POST:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        age = request.POST['age']
        address = request.POST['address']
        email = request.POST['email']
        image = request.FILES.get('image')

        # checking if user wants to change profile too
        if image is not None:
            image = request.FILES.get('image')

        # validating username and age 
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect(f"/update/{request.user.pk}")
        if int(age) < 12:
            messages.error(request, "Age must be greater than 12")
            return redirect(f"/update/{request.user.pk}")
        account.first_name = firstname
        account.last_name = lastname
        account.username = username
        account.age = age
        account.address = address
        account.email = email
        if image:
            account.image = image
        account.save()
    
    # sending data to front end 
    context['id'] = account.id
    context['username'] = account.username
    context['first_name'] = account.first_name
    context['last_name'] = account.last_name
    context['age'] = account.age
    context['email'] = account.email
    context['address'] = account.address
    context['image'] = account.image.url
    return render(request, 'update.html', context)


def posts(request, *args, **kwargs):
    if request.user.is_authenticated:

        user = request.user
        context = {}
        try:
            posts = Post.objects.filter(user=user)
        # In this case may be user hasn't make any post
        except Post.DoesNotExist:
            posts = None
        context['posts'] = posts
        return render(request, 'mypost.html', context)
    else:
        return redirect("/login")

def perticularPost(request, *args, **kwargs):
    if request.user.is_authenticated:
        context = {}
        user = request.user
        postId = kwargs.get('post_id')

        try:
            post = Post.objects.get(pk=postId)
        except Post.DoesNotExist:
            return HttpResponse("Post not found")

        # this will check wheater you are opening your post or others post 
        if user != post.user:
            return HttpResponse("You are not allowed to be here")

        if request.method == "POST":
            winner_name = request.POST['winner']
            post.winner = winner_name
            post.save()
            pass
        try:
            comments = Comment.objects.filter(post=post)
            context['comments'] = comments
        # when no comments are there 
        except Comment.DoesNotExist:
            context['comments'] = None

        context['post'] = post
        return render(request, 'perticularPost.html', context)
    else:
        return redirect("/login")
        

def createpost(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            user = request.user
            description = request.POST['details']
            image = request.FILES.get('image')

            # now creating new post 
            post = Post(user=user, image=image, dsc=description)
            post.save()
            messages.success(request, 'Your post is live now')
    else:
        return redirect("/login")
    return render(request, 'createpost.html')

