from django.contrib import admin
from django.urls import path, include
from pinclone import views
from django_email_verification import urls as mail_urls

urlpatterns = [
    path('',views.index, name='home'),
    path('create/', views.createblog, name='createblog'),
    path('single-post/<int:pk>', views.singlepost, name='singlepost'),
    path('saveblog/', views.saveblog, name='saveblog'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contact/', views.contact, name='contact'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('saveEditprofile/<int:id>', views.saveEditprofile, name='saveEditprofile'),
    path('profile/<int:pk>/', views.userprofile, name='profile'),
    path('contactsave/', views.contactsave, name='contactsave'),
    path('comment-save/<int:pk>/', views.commentsave, name='commentsave'),
    path('comment-pin-save/<int:pk>/', views.commentpinsave, name='commentpinsave'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logoutuser, name='logout'),
    path('picgallery/', views.picgallery, name='picgallery'),
    path('uploadimage/', views.uploadimage, name='uploadimage'),
    path('saveimage/', views.saveimage, name='saveimage'),
    path('susbcribe/', views.subscribe, name='susbcribe'),
    path('searchblog/', views.searchblog, name='searchblog'),
    path('follow/<int:id>/', views.follow, name='follow'),
    path('unfollow/<int:id>/', views.unfollow, name='unfollow'),
    path('pin-photo/<int:id>/', views.pinPhoto, name='pin'),
    path('like/<int:id>/', views.like, name='like'),
    path('unlike/<int:id>/', views.unlike, name='unlike'),
    path('admin/', admin.site.urls),
    path('email/', include(mail_urls)),   
]
