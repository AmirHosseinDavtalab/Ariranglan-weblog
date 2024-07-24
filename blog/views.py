from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, "blog/index.html")


def post_list(request, category=None):
    if category is not None:
        posts = Post.published.filter(category=category)
    else:
        posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {
        'posts': posts,
        'category': category,

    }
    return render(request, 'blog/list.html', context)


# class PostListView(ListView):
#     paginate_by = 3
#     template_name = 'blog/list.html'
#     queryset = Post.published.all()
#     context_object_name = 'posts'


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    form = CommentForm()
    comments = post.comments.filter(active=True)
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'blog/detail.html', context)


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'


def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket_obj = Ticket.objects.create()
            cd = form.cleaned_data
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.name = cd['name']
            ticket_obj.message = cd['message']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
            return redirect('blog:ticket')
    else:
        form = TicketForm()
    return render(request, 'form/ticket.html', {'form': form})


@require_POST
def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.success(request, 'کامنت شما با موفقیت ثبت شد')
        return redirect('blog:post_detail', pk=pk)
    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }
    return render(request, "form/comment.html", context)


def search_post(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results2 = Post.published.annotate(similarity=TrigramSimilarity('description', query)).filter(
                similarity__gt=0.1)
            results1 = Post.published.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1)
            results = (results2 | results1).order_by('-similarity')
    context = {
        'query': query,
        'results': results
    }

    return render(request, 'blog/search.html', context)


@login_required
def profile(request):
    user = request.user
    profile_img = user.profile.photo.url
    posts = Post.published.filter(author=user)
    author = user.username
    context = {
        'posts': posts,
        'profile_img': profile_img,
        'author': author
    }
    return render(request, 'blog/profile.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = PostForm()
    return render(request, 'form/createpost.html', {'form': form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile')
    return render(request, 'form/delete_post.html', {'post': post})


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('blog:profile')


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = PostForm(instance=post)
    return render(request, 'form/edit_post.html', {'form': form, 'post': post})


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('blog:profile')
#                 else:
#                     return HttpResponse('your account is disabled')
#             else:
#                 return HttpResponse('your password or username is wrong')
#     else:
#         form = LoginForm()
#     return render(request, 'form/login.html', {'form':form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, files=request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'registration/edit_profile.html', context)


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = Post.published.filter(author=user)
    context = {
        'user': user,
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'blog/profile_detail.html', context)
