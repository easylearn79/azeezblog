# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from blog.utils import unique_slug_generator
from tinymce import HTMLField
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
from taggit.managers import TaggableManager



User = get_user_model()

# Create your models here.



class Course(models.Model):
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url =models.CharField(max_length=2089, null=True)
    content = HTMLField('content')  
    tags = TaggableManager()
    objects = models.Manager()  # default manager
    newmanager = NewManager() 


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("course_detail", args=[self.slug])
    


def slug_generator(sender, instance, *args, **kwargs):
    """ Generate unique slug """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Course)