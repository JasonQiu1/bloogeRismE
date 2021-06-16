from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.db.models import Q

from .models import Post

def get_visible_posts():
    return Post.objects.filter(
        Q(pub_date__lte=timezone.now()),
        Q(hidden=False)
    )

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """ Get the last 5 past posts """
        return get_visible_posts(
            ).order_by('-pub_date')[:5] 

class PostView(generic.DetailView):
    template_name = 'blog/post.html'
    model = Post

    def get_queryset(self):
        """ Search through past posts only """
        return get_visible_posts()
