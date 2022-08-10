from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from .forms import BlogForm, CommentForm, CommentPinForm, ProfileForm, UserForm, UploadForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django_email_verification import sendConfirm
from django.contrib.auth.decorators import login_required
from Infographic.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

# Create your views here.

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        # Email = request.POST['email']   
        name = request.POST.get('username')
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error':'Email already exists'})
        else: 
            try:
                password1 = request.POST.get('password1')
                password_c = request.POST.get('password2')
                if password1 == password_c:
                    user = User.objects.create_user(username=name, email=email, password=password1)
                    user.save()
                    # sendConfirm(user)
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'signup.html', {'Incorrect':'error'})
            except IntegrityError:
                return render(request, 'signup.html', {'error':'User already exists'})
        
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'error':'Invalid Username/Password'})
        else:
            login(request, user)
            return redirect('home') 

@login_required
def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')

def index(request):
    Blogs = blog.objects.order_by('-created')
    featuredblog = featuredBlog.objects.all()
    context = {
        'blogs':Blogs,
        'featuredBlogs':featuredblog,
    }
    return render(request, 'index.html', context=context)

@login_required
def createblog(request):
    category = Blog_Categorie.objects.all()
    return render(request, 'createblog.html', {'form':BlogForm(),'categories':category})

def singlepost(request,pk):
    Blog = get_object_or_404(blog, pk=pk)
    context = {
        "blog":Blog,
        "form":CommentForm(),
    }
    return render(request, 'single-post.html', context=context)

@login_required
def saveblog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            Form = form.save(commit=False)
            Form.user = request.user
            form.save()
        else:
            return HttpResponse(form.errors)
    return redirect('home')

def aboutus(request):
    return render(request, 'about-us.html')

def Gallery(request):
    image = gallery.objects.all()
    return redirect('home')

def contact(request):
    return render(request, 'contact.html')

@login_required
def editprofile(request):
    context = {
        'form1':UserForm(instance=request.user),
        'form2':ProfileForm(instance=request.user.profile),
    }
    return render(request, 'profile_edit.html', context=context)

@login_required
def saveEditprofile(request,id):
    if request.method == 'POST':
        y = get_object_or_404(profile, id=id, user=request.user)
        form = UserForm(request.POST, instance=request.user)
        form2 = ProfileForm(request.POST, request.FILES, instance=y)
        if form.is_valid():
            Form = form.save(commit=False)
            Form.user = request.user
            Form.save()
        if form2.is_valid():
            form2.save()
        return redirect(request.META['HTTP_REFERER'])

def userprofile(request,pk):
    Profile = get_object_or_404(profile, pk=pk)
    if profile.objects.filter(followers = request.user.id): #logged in user ki id
        follow = True
    else:
        follow = False
    Gallery = gallery.objects.filter(user=Profile.user)
    context = {                 
        'profile':Profile,
        'follow' :follow,
        'Gallery':Gallery
    }
    return render(request, 'profile.html', context=context)

def follow(request,id):
    user = get_object_or_404(profile, id=id)
    user.followers.add(request.user)
    request.user.profile.following.add(user.user)
    return redirect(request.META['HTTP_REFERER']) #Returns me to the same page/back to that page

def unfollow(request,id):
    user = get_object_or_404(profile, id=id)
    user.followers.remove(request.user)
    request.user.profile.following.remove(user.user)
    return redirect(request.META['HTTP_REFERER']) #Returns me to the same page/back to that page

def contactsave(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    Contact.objects.create(name=name,email=email,subject=subject,message=message)
    return render(request, 'contact.html')

@login_required
def commentsave(request, pk):
    Blog = get_object_or_404(blog, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid:
            Form = form.save(commit=False)
            Form.blog = Blog
            Form.blog_comment_user = request.user
            Form.save()
            return redirect(request.META['HTTP_REFERER'])

def commentpinsave(request, pk):
    Pin = get_object_or_404(gallery, pk=pk)
    if request.method == 'POST':
        form = CommentPinForm(request.POST)
        if form.is_valid:
            Form = form.save(commit=False)
            Form.pin = Pin
            Form.pin_comment_user = request.user
            Form.save()
            return redirect(request.META['HTTP_REFERER'])

def picgallery(request):
    Gallery = gallery.objects.all()  
    c1 = {'Gallery': Gallery, 'form':UploadForm()}
    return render(request, 'picgallery.html', context=c1)

def uploadimage(request):
    context = {
        'form':UploadForm(),
    }
    return render(request, 'upload.html', context=context)

def saveimage(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            Form = form.save(commit=False)
            Form.user = request.user
            Form.save()
            return redirect('picgallery')

def subscribe(request):
    if request.method == 'POST':
        sub = (request.POST.get('email'))
        subject = 'Welcome to Infographic'
        message = 'Thanks for subscribing!'
        recepient = str(sub)
        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'success.html', {'recepient': recepient})
    return render(request, 'index.html', {'form':sub})

def searchblog(request):
    qur = request.GET.get('search')
    print(qur)
    print(qur)
    print(qur)
    print(qur)
    blogs = blog.objects.filter(text__contains = qur)
    context = {
        'qur':blogs,
    }
    return render(request, 'searchblog.html', context=context)

def pinPhoto(request,id):
    photo = get_object_or_404(gallery,id=id)
    if gallery.objects.filter(likes = request.user.id):
        liked = True
    else:
        liked = False
    return render(request, 'pin-photo.html', {'photo':photo,'liked':liked})

def like(request,id):
    like = get_object_or_404(gallery,id=id)
    like.likes.add(request.user)
    return redirect(request.META['HTTP_REFERER']) #Returns me to the same page/back to that page

def unlike(request,id):
    unlike = get_object_or_404(gallery,id=id)
    unlike.likes.remove(request.user)
    return redirect(request.META['HTTP_REFERER']) #Returns me to the same page/back to that page