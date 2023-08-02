from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from forum.models import *
from forum.forms import *

menu = [
    {"text": "О сайте", "link": "about"},
    {"text": "Добавить пост", "link": "addpage"}
]


def index(request):
    cats = Categories.objects.all()
    posts = Posts.objects.filter(is_published=True)

    context = {
        "title": "Главная страница",
        "posts": posts,
        "cat_selected": 0
    }

    return render(request, "forum/index.html", context=context)


def category(request, cat_slug):
    categories = Categories.objects.all()
    c = categories.get(slug=cat_slug)
    posts = Posts.objects.filter(cat_id=c.pk, is_published=True)

    context = {
        "title": "Страница категории",
        "posts": posts,
        "cat_selected": c.pk,
    }

    return render(request, "forum/index.html", context=context)


def post(request, post_id):
    cats = Categories.objects.all()
    post = Posts.objects.get(pk=post_id)
    comments = Comments.objects.filter(post_id=post_id, is_approved=True)
    if request.user in Users.objects.all():
        if not(request.user in post.views.all()):
            post.views.add(request.user)

    
    if request.method == 'POST':
        form = AddCommentForm(data=request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.recipient = post.author
            f.post = post
            f.save()
            return redirect('post', post_id=post_id)
    else:
        form = AddCommentForm()

    context = {
        "title": "Страница поста",
        "post": post,
        "comments": comments,
        "cat_selected": post.cat_id,
        "form": form
    }

    return render(request, "forum/post.html", context=context)

@login_required
def addPage(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.save()
            return redirect("home")
    else:
        form = AddPostForm()
    context = {"form": form, "title": "Добавить пост"}
    return render(request, "forum/addpage.html", context=context)

def edit_post(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)

    if request.method == "POST":
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post", post_id=post_id)
    else:
        form = EditPostForm(instance=post)

    context = {"form": form, "post": post}
    return render(request, "forum/edit_post.html", context)

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)

    if request.method == "POST":
        form = AddCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            post_id = comment.post_id
            return redirect("post", post_id=post_id)
    else:
        form = AddCommentForm(instance=comment)

    context = {"form": form, "comment": comment}
    return render(request, "forum/edit_comment.html", context)

def about(request):
    context = {
        "title": "Страница о сайте",
    }
    return render(request, 'forum/about.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def register(request):   
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = RegisterUserForm()
        
    context = {
        "title": "Регистрация",
        "form": form
    }
    return render(request, "forum/register.html", context)
    
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    
    context = {'title': 'Авторизация', 'form': form}
    return render(request, 'forum/login.html', context)

def like_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    elif request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
        post.likes.add(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post', post_id=post_id)

def dislike_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    elif request.user in post.likes.all():
        post.likes.remove(request.user)
        post.dislikes.add(request.user)
    else:
        post.dislikes.add(request.user)

    return redirect('post', post_id=post_id)

def like_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    post_id = comment.post_id
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    elif request.user in comment.dislikes.all():
        comment.dislikes.remove(request.user)
        comment.likes.add(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('post', post_id=post_id)

def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    post_id = comment.post_id
    if request.user in comment.dislikes.all():
        comment.dislikes.remove(request.user)
    elif request.user in comment.likes.all():
        comment.likes.remove(request.user)
        comment.dislikes.add(request.user)
    else:
        comment.dislikes.add(request.user)
    return redirect('post', post_id=post_id)

def delete_post(request, post_id):
    try:
        post = Posts.objects.get(pk=post_id)
    except:
        pass

    if request.method == "POST":
        try:
            post.delete()
        except:
            pass
        return redirect("home")

    context = {"post": post}
    return render(request, "forum/delete_post.html", context)

def delete_comment(request, comment_id, post_id):
    try:
        comment = Comments.objects.get(pk=comment_id)
    except Comments.DoesNotExist:
        pass

    if request.method == "POST":
        try:
            comment.delete()
        except:
            pass
        return redirect("post", post_id=post_id)  

    context = {"comment": comment}
    return render(request, "forum/delete_comment.html", context)

def logout_user(request):
    logout(request)
    return redirect('login')
    
