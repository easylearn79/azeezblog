from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from post.models import Post
from django.utils.feedgenerator import Atom1Feed


class LatestPostsFeed(Feed):
    title = 'Learnwell'
    link = ''
    description = 'New posts of Learnwell'


    def items(self):
        return Post.objects.filter(status='published')

    def item_title(self, item):
        return item.title


    def item_description(self, item):
        return truncatechars(item.content,30)




class MyFeed(Feed):
    feed_type = Atom1Feed