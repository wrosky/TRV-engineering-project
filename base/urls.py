from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('', views.home, name='home'),
    path('post/<str:pk>/', views.post, name='post'),
    path('profile/<str:username>/', views.profilePage, name='user_profile'),

    path('create_post/', views.createPost, name='create_post'),
    path('update_post/<str:pk>', views.updatePost, name='update_post'),
    path('delete_post/<str:pk>', views.deletePost, name='delete_post'),
    path('delete_comment/<str:pk>', views.deleteComment, name='delete_comment')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)