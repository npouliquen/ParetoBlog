from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm

# Create your views here.


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blogpost/post_list.html', {'posts': posts})


def single_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Post.objects.get(id=post_id)
    if post.published_date == None:
        raise Http404("There is no published post with that id")
    return render(request, 'blogpost/single_post.html', {'post': post})


@login_required(login_url='/login/')
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('single_post', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'blogpost/new_post.html', {'form': form})


@login_required(login_url='/login/')
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('single_post', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blogpost/edit_post.html', {'form': form})


@login_required(login_url='/login/')
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('/')


def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        url = request.META.get('HTTP_REFERER')
        index = url.find('=')
        if index >= 0:
            url = url[index + 1:]
        else:
            url = '/'

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(url)
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'blogpost/login.html',)


def user_logout(request):
    logout(request)
    return redirect('/')
