from django.shortcuts import render, redirect,get_object_or_404, redirect
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # use Django's built-in User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post , Comment
from .forms import PostForm ,CommentForm
from django.urls import reverse_lazy
from django.db.models import Q
from taggit.models import Tag

# -----------------------------
# Registration View
# -----------------------------
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'blog/register.html', {'form': form})

# -----------------------------
# Login View
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid username")
            return redirect('login')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid password")
            return redirect('login')
        else:
            auth_login(request, user)
            return redirect('home')  # redirect to your home page

    return render(request, 'blog/login.html')  # template path matches blog folder

# -----------------------------
# Profile View (editable)
# -----------------------------
@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'blog/profile.html', {'form': form})



# List all posts (public)
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # template path
    context_object_name = 'posts'
    paginate_by = 5  # optional

# View post detail (public)
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# Create post (authenticated only)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update post (author only)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete post (author only)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
# -------------------------
# Add a comment
# -------------------------
 
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

# -------------------------
# Update Comment
# -------------------------
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

# -------------------------
# Delete Comment
# -------------------------
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
    
def search_posts(request):
    query = request.GET.get('q')
    results = Post.objects.none()
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'blog/search_results.html', {'results': results, 'query': query})

def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__slug=tag_slug)
    return render(request, 'blog/tag_posts.html', {'tag': tag, 'posts': posts})

class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/tag_posts.html'  # template for posts by tag
    context_object_name = 'posts'
    paginate_by = 10  # optional: paginate if many posts

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags__slug=tag_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context