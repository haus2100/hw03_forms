from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.shortcuts import redirect


from .models import Group, Post

from .forms import PostForm

User = get_user_model()


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    posts = group.group_posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.filter(author=author)
    posts_list = Post.objects.filter(author=author).order_by('-pub_date')
    posts_count = Post.objects.filter(author=author).count()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'posts': posts,
        'posts_count': posts_count,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post_id = Post.objects.get(pk=post_id)
    posts_count = Post.objects.filter(author_id=post_id.author_id).count()
    context = {
        'post_id': post_id,
        'posts_count': posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        text = form.cleaned_data['text'],
        group = form.cleaned_data['group'],
        form.text = text
        form.group = group
        form.instance.author = request.user
        form.save()
        return redirect('posts:profile', request.user)
    return render(request, template, {'form': form})


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    is_edit = True
    if form.is_valid() and post.author == request.user:
        post = form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'is_edit': is_edit,
        'post': post,
    }
    return render(request, 'posts/create_post.html', context)
