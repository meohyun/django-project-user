from . import views
from django.urls import path

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path(
        'email_confirmation/',
        views.TemplateView.as_view(template_name='account/email_confirmation_required.html'),
        name = 'required'),
    path(
        'email_confirmation_done/',
        views.TemplateView.as_view(template_name='account/email_confirmation_done.html'),
        name = 'confirmation_done'),
    # zokbo
    path('zokbo/<int:pk>/',views.DetailZokboView.as_view(),name='detail'),
    path('zokbo_upoload/',views.CreateZokboView.as_view(),name ='create'),
    path('zokbo/<int:pk>/update',views.UpdateZokboView.as_view(),name ='update'),
    path('zokbo/<int:pk>/delete',views.DeleteZokboView.as_view(),name ='delete'),
    path('zokbo/<int:pk>/download',views.download,name='download'),
    path('zokbo-list/',views.ListZokboView.as_view(),name='list'),

    # profile
    path('profile/<int:user_id>/',views.ProfileView.as_view(),name= 'profile'),
    path('profile/<int:user_id>/reviews/',views.UserReviewListView.as_view(),name='user-review-list'),
    path('profile-set/',views.ProfileSetView.as_view(),name= 'profile-set'),
    path('edit-profilet',views.ProfileUpdateView.as_view(),name='profile-update'),

    # search
    path('search/',views.search,name='search'),

    # comment
    path('comments/<int:post_pk>',views.comment_new,name='comment-new'),
    path('comments/<int:post_pk>/edit/<int:pk>',views.comment_update,name='comment-update'),
    path('comments/<int:post_pk>/delete/<int:pk>',views.comment_delete,name='comment-delete'),

    # signout
    path('delete/user',views.signout,name="signout"),

    # like
    path('post-like/<int:post_id>/',views.post_like,name="post-like"),

    # password
    path('password_change/',views.change_password,name='password-change')
]

