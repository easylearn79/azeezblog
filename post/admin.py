from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Author, Post, Comment 
  
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment, MPTTModelAdmin)
