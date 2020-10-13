# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.shortcuts import render
from .models import Course
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect, reverse
from hitcount.views import HitCountDetailView
from taggit.models import Tag
# Create your views here.






class CourseListView(ListView):
    model = Course
    template_name = 'index.html'
    context_object_name = 'courses'
    ordering = ['-publish']
    paginate_by = 4
    

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        common_tags = Course.tags.most_common()[:4]
        context['common_tags'] = common_tags
        return context


class CourseDetailView(HitCountDetailView):
    model = Course
    template_name = 'course_detail.html'
    slug_url_kwarg = 'django_slug'
    slug_url_kwarg = "slug"
    slug_field = 'slug'
    count_hit = True


    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        return context





def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    courses = Course.objects.filter(tags=tag)

    context = {
        'tag':tag,
        'courses':courses,
    }
    return render(request, 'index.html', context)