from django.db import models
from tinymce import HTMLField
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from blog.utils import unique_slug_generator
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import pre_save
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
from taggit.managers import TaggableManager
from cloudinary.models import CloudinaryField
from meta.models import ModelMeta


# Create your models here.


STATUS = ((0, "Draft"), (1, "Publish"))

User = get_user_model()


class Photo(models.Model):
  image = CloudinaryField('image')

  
  






class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=2089)
    comment_image = models.CharField(max_length=2089)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=250, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Post(ModelMeta,models.Model):
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=100)
    overview = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250, blank=True, unique_for_date='publish')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=2089, null=True, blank=True)
    image = CloudinaryField('image')
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.PROTECT, default='uncategorized', blank=True)
    content = HTMLField('content')
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=10, choices=options, default='draft')
    tags = TaggableManager()
    objects = models.Manager()  # default manager
    newmanager = NewManager()
    #   comments = GenericRelation(Comment)


    _metadata = {
        'title': 'title',
        'description': 'overview',
        "image": "get_image_full_url",
        "image_width": "get_image_width",
        "image_height": "get_image_height",
    }

    def get_meta_image(self):
        if self.image:
            return self.image.url
            

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug])

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()


def slug_generator(sender, instance, *args, **kwargs):
    """ Generate unique slug """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Post)


class Comment(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['publish']

    def __str__(self):
        return 'Comment {} by {}'.format(self.content, self.name)
