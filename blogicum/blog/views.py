

import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count

from blog.models import Post, Category, Comment
from .forms import CommentForm, PostForm, UserForm


NUMBER_OF_POSTS = 10


def index(request):
    template_name = 'blog/index.html'
    today = datetime.datetime.today()
    post_list = Post.objects.filter(is_published=True,
                                    category__is_published=True,
                                    pub_date__lte=today
                                    ).order_by('-pub_date'
                                               ).annotate(
                                                   comment_count=Count(
                                                       'comments'))
    paginator = Paginator(post_list, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    today = datetime.datetime.today()
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        post = get_object_or_404(Post, is_published=True,
                                 pub_date__lte=today,
                                 category__is_published=True,
                                 pk=post_id)
    comments = post.comments.all()
    context = {'post': post,
               'form': CommentForm(files=request.FILES or None),
               'comments': comments}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    today = datetime.datetime.today()
    show_category = get_object_or_404(Category.objects.filter(
        slug=category_slug, is_published=True))
    posts = show_category.posts.filter(is_published=True,
                                       pub_date__lte=today
                                       ).order_by('-pub_date'
                                                  ).annotate(
                                                      comment_count=Count(
                                                          'comments'))
    paginator = Paginator(posts, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': show_category,
               'page_obj': page_obj}
    return render(request, template_name, context)


@login_required
def create_post(request):
    template_name = 'blog/create.html'
    form = PostForm(request.POST or None, request.FILES or None)
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        redirect_page = reverse('blog:profile', args=[request.user])
        return redirect(redirect_page)
    return render(request, template_name, context)


def profile(request, username):
    template_name = 'blog/profile.html'
    user = get_object_or_404(User.objects.filter(username=username))
    posts = Post.objects.filter(author=user).order_by('-pub_date'
                                                      ).annotate(
                                                          comment_count=Count(
                                                              'comments'))
    paginator = Paginator(posts, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': user,
               'page_obj': page_obj}
    return render(request, template_name, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id)


@login_required
def edit_profile(request):
    template_name = 'blog/user.html'
    instance = request.user
    form = UserForm(request.POST, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, template_name, context)


def edit_post(request, post_id):
    instance = get_object_or_404(Post, pk=post_id)
    if instance.author != request.user:
        return redirect(to='blog:post_detail', post_id=post_id)
    template_name = 'blog/create.html'
    form = PostForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        redirect_page = reverse('blog:post_detail', args=[post_id])
        return redirect(redirect_page)
    return render(request, template_name, context)


@login_required
def delete_post(request, post_id):
    template_name = 'blog/create.html'
    instance = get_object_or_404(Post, pk=post_id, author=request.user)
    form = PostForm(request.POST or None, instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        redirect_page = reverse('blog:index')
        return redirect(redirect_page)
    return render(request, template_name, context)


@login_required
def edit_comment(request, post_id, comment_id):
    template_name = 'blog/comment.html'
    redirect_page = reverse('blog:post_detail', args=[post_id])
    instance = get_object_or_404(Comment, pk=comment_id, author=request.user,
                                 post__id=post_id)
    form = CommentForm(request.POST or None, instance=instance)
    context = {'form': form,
               'comment': instance}
    if form.is_valid():
        instance = form.save()
        instance.save()
        return redirect(redirect_page)
    return render(request, template_name, context)


@login_required
def delete_comment(request, post_id, comment_id):
    template_name = 'blog/comment.html'
    redirect_page = reverse('blog:post_detail', args=[post_id])
    instance = get_object_or_404(Comment, pk=comment_id, author=request.user,
                                 post__id=post_id)
    context = {'comment': instance}
    if request.method == 'POST':
        instance.delete()
        return redirect(redirect_page)
    return render(request, template_name, context)
