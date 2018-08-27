# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.views.generic.edit import ModelFormMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostForm, CommentForm, LoginForm


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = "latest_posts_list"
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.order_by('-pub_date')


class DetailsView(generic.DetailView):
    model = Post
    template_name = "blog/details.html"


class EditView(generic.UpdateView):
    model = Post
    fields = ['text', 'title']
    template_name_suffix = "_update_form"


class CreatePostView(generic.CreateView):
    model = Post
    fields = ["text", "title"]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.pub_date = timezone.now()
        self.object.author = self.request.user
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)


class DeletePostView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')


class CreateCommentView(generic.CreateView):
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.pub_date = timezone.now()
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        self.object.post = post
        self.object.author = self.request.user
        return super(CreateCommentView, self).form_valid(form)

    def get_success_url(self):
        post_id = self.kwargs['pk']
        return reverse_lazy("blog:details", kwargs={"pk": post_id})


class DeleteCommentView(generic.DeleteView):
    model = Comment
    success_url = reverse_lazy('blog:index')

    def get_success_url(self):
        post_id = self.kwargs['post_pk']
        return reverse_lazy("blog:details", kwargs={"pk": post_id})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated ' \
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'blog/templates/registration/login.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'blog/profile.html', {"user": request.user})
