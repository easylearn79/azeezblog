from django.contrib.sitemaps import Sitemap
from post.models import Post
from course.models import Course

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.publish

class CourseSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Course.objects.filter()


    def lastmod(self, obj):
        return obj.publish

