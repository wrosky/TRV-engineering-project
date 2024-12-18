from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="base/password_reset/password_reset.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="base/password_reset/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="base/password_reset/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="base/password_reset/password_reset_done.html"), name='password_reset_complete'),

    path('', views.home, name='home'),
    path('post/<str:pk>/', views.post, name='post'),
    path('profile/<str:username>/', views.profilePage, name='user_profile'),
    path('edit_user/', views.editUser, name='edit_user'),

    path('create_post/', views.createPost, name='create_post'),
    path('update_post/<str:pk>', views.updatePost, name='update_post'),
    path('delete_post/<str:pk>', views.deletePost, name='delete_post'),
    path('delete_comment/<str:pk>', views.deleteComment, name='delete_comment'),
    path('like/<str:pk>', views.like, name='like'),

    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
    path('cancel_friend_request/<int:request_id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('remove_friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('search-non-friends/', views.search_non_friends, name='search_non_friends'),

    path('chat/', views.chat, name='chat'),
    path('friend_chats/', views.friend_chats, name='friend_chats'),
    path('chat/<int:friend_id>/', views.private_chat, name='private_chat'),

    path('trips/', views.list_trips, name='list_trips'),
    path('trips/create/', views.create_trip, name='create_trip'),
    path('trips/<int:pk>/', views.trip_detail, name='trip_detail'),
    path('trips/<int:pk>/update/', views.update_trip, name='update_trip'),
    path('trip/<int:pk>/download_pdf/', views.download_trip_pdf, name='download_trip_pdf'),
    path('trip/<int:pk>/delete/', views.deleteTrip, name='delete_trip'),


    path('search-flight/', views.search_flight, name='search_flight'),
    path('airport-autocomplete/', views.airport_autocomplete, name='airport_autocomplete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)