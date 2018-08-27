from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

app_name = "blog"

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = "index"),
    url(r'profile/$', views.profile, name= 'profile'),
    url(r'login/$', auth_views.LoginView.as_view(), name="login"),
    url(r'logout/$', auth_views.LogoutView.as_view(), name="logout"),
    url(r'post/(?P<pk>[0-9]+)/$', views.DetailsView.as_view(), name="details"),
    url(r'post/(?P<pk>[0-9]+)/edit/$', login_required(views.EditView.as_view()), name="edit_post"),
    url(r'post/(?P<pk>[0-9]+)/comment/$', login_required(views.CreateCommentView.as_view()), name="comment_new"),
    url(r'post/(?P<post_pk>[0-9]+)/comment/(?P<pk>[0-9]+)/delete/$', login_required(views.DeleteCommentView.as_view()), name="delete_comment"),
    url(r'post/(?P<pk>[0-9]+)/delete/$', login_required(views.DeletePostView.as_view()), name="delete_post"),
    url(r'post/new/$', login_required(views.CreatePostView.as_view()), name = "post_new")

]