from store.models.models import Post, Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)

from django.shortcuts import (
render_to_response
)
from django.template import RequestContext

# HTTP Error 400
def bad_request(request, exception):
    response = render_to_response(
        '400.html',
        context_instance=RequestContext(request)
        )

    response.status_code = 400

    return response

# HTTP Error 500
def server_error(request):
    context = {}
    response = render(request, "404.html", context=context)
    response.status_code = 500
    return response

# HTTP Error 404
def page_not_found(request, exception):
    response = render_to_response(
        '404.html',
        context_instance=RequestContext(request)
        )

    response.status_code = 404

    return response

# HTTP Error 403
def permission_denied(request, exception):
    response = render_to_response(
        '403.html',
        context_instance=RequestContext(request)
        )

    response.status_code = 403

    return response

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5


    def get_queryset(self):
        try:
            keyword = self.request.GET['q']
        except:
            keyword = ''
        if (keyword != ''):
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword))
        else:
            object_list = self.model.objects.all()
        return object_list


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post 
    template_name = 'blog/post_detail.html'
    context_object_name='posts'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    context_object_name='blog'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    context_object_name='blog'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'
    context_object_name='blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About','blog':blog})


@login_required(login_url='login')
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get('user_id'))
        text = request.POST.get('text')
        Comment(author=user, post=post, text=text).save()
        messages.success(request, "Your comment has been added successfully.")
    else:
        return redirect('post_detail', pk=pk)
    return redirect('post_detail', pk=pk)
