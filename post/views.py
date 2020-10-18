from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from .models import Post, User, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import NewCommentForm, PostSearchForm
from django.db.models import Q
from taggit.models import Tag


class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'
    ordering = ['-publish']
    paginate_by = 4
    count_hit = True

    def get_context_data(self, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostListView, self).get_context_data(**kwargs)
        most_recent = Post.objects.order_by('-publish')[:4]
        context['most_recent'] = most_recent
        common_tags = Post.tags.most_common()[:4]
        context['common_tags'] = common_tags
        context['cat_menu'] = cat_menu
        return context

    # class PostDetailView(DetailView):
    # model = Post
    # template_name = 'post_detail.html'
    # context_object_name = 'post'




def post_detail(request, post):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=post, status='published')
    cat_menu = Category.objects.all()
    most_recent = Post.objects.order_by('-publish')[:4]
    allcomments = post.comments.filter(status=True)
    common_tags = Post.tags.most_common()[:4]
    page = request.GET.get('page', 1)
    paginator = Paginator(allcomments, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = NewCommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            return HttpResponseRedirect('/' + post.slug)
    else:
        comment_form = NewCommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'allcomments': allcomments,
                                           'comment_form': comment_form,
                                           'common_tags': common_tags,
                                           'most_recent': most_recent,
                                           'cat_menu': cat_menu})


def post_search(request):
    cat_menu = Category.objects.all()
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(image_url__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset,
        'cat_menu': cat_menu
    }
    return render(request, 'search.html', context)


def tagged(request, slug):
    cat_menu = Category.objects.all()
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = Post.tags.most_common()[:4]
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'common_tags': common_tags,
        'posts': posts,
        'cat_menu': cat_menu
    }
    return render(request, 'blog.html', context)


class CategoryListView(ListView):
    template_name = 'category_list.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_menu_list = Category.objects.all()
        context["cat_menu_list"] = cat_menu_list
        return context
    
    


def CategoryView(request, slug):
    cat_menu = Category.objects.all()
    category = Category.objects.get(slug=slug)
    context = {
        'category': category,
        'cat_menu': cat_menu
    }
    return render(request, 'category.html', context)

