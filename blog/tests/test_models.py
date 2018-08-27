
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from blog.models import Post, Comment


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="admin", email="admin@example.com", password="adminadmin")
        Post.objects.create(author=user, text="text", title="title", pub_date=timezone.now())

    def test_text_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('text').verbose_name
        self.assertEquals(field_label, "text")

    def test_title_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEquals(field_label, "title")

    def test_author_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('author').verbose_name
        self.assertEquals(field_label, "author")

    def test_date_published_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('pub_date').verbose_name
        self.assertEquals(field_label, 'date published')

    def test_object_name_is_title(self):
        post = Post.objects.get(id=1)
        expected_object_name = post.title
        self.assertEquals(expected_object_name, str(post))

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEquals(post.get_absolute_url(), reverse('blog:details', kwargs={"pk":1}))

class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass