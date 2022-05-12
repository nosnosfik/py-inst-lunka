from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from posts.models import Post, Like, Comment
from django.contrib import messages


class PostList(generic.ListView):
    model = Post
    paginate_by = 10
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        return context


class PostCreate(generic.CreateView):
    model = Post
    fields = ['image', 'description']
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDelete(generic.DeleteView):
    model = Post
    success_url = reverse_lazy("home")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(PostDelete, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        return obj


def like(request, pk):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        post = Post.objects.get(id=pk)
        if user in post.user_like.all():
            messages.info(request, f"You already liked it!")
            return redirect('home')
        new_like = Like(post=post, author=user)
        new_like.already_liked = True

        post.like += 1
        post.user_like.add(user)
        post.save()
        new_like.save()
        messages.info(request, f"New like, new day!")
        return redirect('home')


def comment(request, pk):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        post = Post.objects.get(id=pk)
        text = request.POST.get('text_comment')
        new_comment = Comment(post=post, author=user, text=text)
        new_comment.save()
        return redirect('home')
