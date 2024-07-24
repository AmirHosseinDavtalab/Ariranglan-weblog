from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<pk>', views.post_detail, name='post_detail'),
    path('posts/category/<str:category>', views.post_list, name='post_list_category'),
    path('posts/<pk>/comment', views.post_comment, name='post_comment'),
    path('ticket', views.ticket, name='ticket'),
    path('search/', views.search_post, name='search_post'),
    path('profile/', views.profile, name='profile'),
    path('profile/detail/<str:username>/', views.profile_detail, name='profile_detail'),
    path('profile/createpost', views.create_post, name='createpost'),
    path('profile/createpost/<pk>', views.edit_post, name='edit_post'),
    path('profile/delete_image/<image_id>', views.delete_image, name='delete_image'),
    path('profile/delete_post/<pk>', views.delete_post, name='delete_post'),
    # path('login', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password-change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password-change-done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/blog/password-reset/complete'), name='password-reset-confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('register/',views.register, name='register'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
]

