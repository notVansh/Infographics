from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField
from django.db.models.signals import post_save

# Create your models here.

class Blog_Categorie(models.Model):
    categoryTitle = models.CharField(max_length=100)

    def __str__(self):
        return self.categoryTitle


class blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog', null=True, blank=True)
    text= models.TextField()
    title= models.CharField(max_length=122, null=True, default='')
    image = models.FileField(upload_to='images/')
    created = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Blog_Categorie, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.title

class Blog_comments(models.Model):
    blog_comments = models.TextField(null=True)
    blog_comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(blog, on_delete=models.CASCADE, default='', related_name='Comment', blank=True, null=True)
    blog_comment_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.blog_comment_user)

class featuredBlog(models.Model):
    blogFeatured = models.ForeignKey(blog, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.blogFeatured)

class gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to='images/',null=True , blank=True)
    caption = models.TextField()
    likes = models.ManyToManyField(User, null=True, blank=True, default='', related_name='liked')

    def __str__(self):
        return self.caption

class pin_comment(models.Model):
    pin_comments = models.TextField(null=True)
    pin_comment_user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    pin = models.ForeignKey(gallery, on_delete=models.CASCADE, default='', related_name='Comments', blank=True, null=True)
    pin_comment_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.pin_comment_user)

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    subject = models.TextField(max_length=54)
    message = models.TextField(max_length=254)
    
    def __str__(self):
        return self.name

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=True, null=True)
    desc = models.TextField(null=True)
    pfp = models.ImageField(default='profile.png', upload_to='profile_pics/', null=True, blank=True)
    cover = models.ImageField(default='cover.png', upload_to='cover_pics/', null=True, blank=True)
    followers = models.ManyToManyField(User, blank=True, null=True, related_name='friended')
    following = models.ManyToManyField(User, blank=True, null=True, related_name='follows', default='')

    def __str__(self):
        return str(self.user)

    def create_profile(sender,instance,created,**kwargs):
        if created:
            profile.objects.create(user=instance)

    post_save.connect(create_profile, sender=User)   