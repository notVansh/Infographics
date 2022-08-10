from pinclone.models import blog
from django.contrib import admin
from .models import *

# Register your models here.
# class PostCreated(admin.ModelAdmin):
#     readonly_fields = ('created', )


class AdminComment(admin.ModelAdmin):
  list_display = ['blog_comments','blog_comment_user','blog']

admin.site.register(blog)
admin.site.register(Contact)
admin.site.register(Blog_Categorie)
admin.site.register(featuredBlog)
admin.site.register(Blog_comments, AdminComment)
admin.site.register(profile)
admin.site.register(gallery)
admin.site.register(pin_comment)