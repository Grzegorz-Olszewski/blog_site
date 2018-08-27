from django.test import TestCase, SimpleTestCase
from blog.models import Post, Comment
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


class PostIndexViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="admin", email="admin@example.com", password="adminadmin")
        Post.objects.create(author=user, text="text", title="title", pub_date=timezone.now())

    def test_index_view_exists(self):
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse("blog:index"))
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_get_post_in_post_list(self):
        response = self.client.get(reverse("blog:index"))
        self.assertEquals(response.context['latest_posts_list'][0].title, "title")

class PostCreateViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="admin", email="admin@example.com", password="adminadmin")
        user.save()

    def test_redirect_to_login_page_if_not_logged_in(self):
        response = self.client.get(reverse("blog:post_new"))
        self.assertRedirects(response, '/login/?next=/post/new/')

    def test_get_to_create_page_if_logged_in(self):
        login = self.client.login(username="admin", password="adminadmin")
        response = self.client.get(reverse("blog:post_new"))
        self.assertTemplateUsed(response, 'blog/post_form.html')

class PostEditViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="admin", email="admin@example.com", password="adminadmin")
        user.save()

    def test_edit_post_redirect_to_login_page_if_not_logged_in(self):
        user = User.objects.get(id=1)
        post = Post.objects.create(title="title", text="text", author=user, pub_date=timezone.now())
        response = self.client.get(reverse("blog:edit_post", kwargs={"pk":post.id}))
        self.assertRedirects(response, '/login/?next=/post/{}/edit/'.format(post.id))

    def test_get_to_edit_page_if_logged_in(self):
        login = self.client.login(username="admin", password="adminadmin")
        user = User.objects.get(id=1)
        post = Post.objects.create(title="title", text="text", author=user, pub_date=timezone.now())
        response = self.client.get(reverse("blog:edit_post", kwargs={"pk": post.id}))
        self.assertTemplateUsed(response, 'blog/post_update_form.html')