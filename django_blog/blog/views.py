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
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

# -------------------------
# Edit a comment
# -------------------------
@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        messages.error(request, "You are not allowed to edit this comment.")
        return redirect('post-detail', pk=comment.post.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully!")
            return redirect('post-detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/comment_form.html', {'form': form})

# -------------------------
# Delete a comment
# -------------------------
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        messages.error(request, "You are not allowed to delete this comment.")
        return redirect('post-detail', pk=comment.post.pk)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
        return redirect('post-detail', pk=comment.post.pk)

    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})
