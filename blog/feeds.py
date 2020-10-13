from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from post.models import Post
from course.models import Course
from django.utils.feedgenerator import Atom1Feed


class LatestPostsFeed(Feed):
    title = 'Abdul Blog'
    link = ''
    description = 'New posts of Abdul Blog'


    def items(self):
        return Post.objects.filter(status='published')

    def item_title(self, item):
        return item.title


    def item_description(self, item):
        return truncatechars(item.content,30)

class LatestCourseFeed(Feed):
    title = ' Course'
    link = ''
    description = 'New Course'

    def items(self):
        return Course.objects.filter()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatechars(item.content, 30)



class MyFeed(Feed):
    feed_type = Atom1Feed