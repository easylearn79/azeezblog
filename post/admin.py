from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Author, Post, Comment,Category,Photo
  
admin.site.register(Author)
admin.site.register(Photo)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment, MPTTModelAdmin)
