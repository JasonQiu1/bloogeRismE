import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

from .models import Post

def make_post(days=0, pub_date=timezone.now(), title_text="Post number ", body="<p>Body text.</p>", hidden=False): 
    """ Make a post days days in the future """
    post_date = pub_date+datetime.timedelta(days=days)
    title = title_text + str(post_date)
    return Post.objects.create(
        pub_date=post_date,
        hidden=hidden,
        title_text=title,
        slug = slugify(title),
        body=body,
    )

def get_response(self, url, args=[]):
    return self.client.get(reverse(url, args=args)) 

# Create your tests here.
class PostModelTests(TestCase):
    def test_post_str(self):
        """ Post conversion to string should return its slug """
        title = "test_post_str test title"
        post = Post.objects.create(
            pub_date=timezone.now(),
            title_text=title,
            slug=slugify(title),
            body="body",
        )
        self.assertEqual(str(post), slugify(title))
        self.assertEqual(str(post), post.slug)

class IndexViewTests(TestCase):
    def test_no_posts(self):
        """ If there are no posts, a default page should be displayed """
        response = get_response(self, 'blog:index')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no posts yet!")
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            [],
        )

    def test_old_post(self):
        """ An old post should show up with both title and body text """
        post = make_post()
        response = get_response(self, 'blog:index')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title_text)
        self.assertContains(response, post.body)
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            [post],
        )

    def test_scheduled_post(self):
        """ Future posts should not show up """
        post = make_post(1)
        response = get_response(self, 'blog:index')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no posts yet!")
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            [],
        )

    def test_past_and_scheduled_post(self):
        """ Past posts should still show up even if there are future posts """
        make_post(1)
        post = make_post(-1)
        response = get_response(self, 'blog:index')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title_text)
        self.assertContains(response, post.body)
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            [post],
        )

class PostViewTests(TestCase):
    def test_nonexistent_post(self):
        """ Accessing a nonexistent slug should 404 """
        response = get_response(self, 'blog:post', ['nonexistent-post'])
        self.assertEqual(response.status_code, 404)

    def test_old_post(self):
        """ Accessing an old slug should show up """
        post = make_post(-1)
        response = get_response(self, 'blog:post', [post])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title_text)
        self.assertContains(response, post.body)

    def test_scheduled_post(self):
        """ Future posts should not show up """
        post = make_post(1)
        response = get_response(self, 'blog:post', [post])
        self.assertEqual(response.status_code, 404)

    def test_hidden_old_post(self):
        """ Hidden old posts should not show up """
        post = make_post(-1, hidden=True)
        response = get_response(self, 'blog:post', [post])
        self.assertEqual(response.status_code, 404)

    def test_hidden_scheduled_post(self):
        """ Hidden future posts should not show up as well """
        post = make_post(1, hidden=True)
        response = get_response(self, 'blog:post', [post])
        self.assertEqual(response.status_code, 404)
