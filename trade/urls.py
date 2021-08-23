from . import views
from django.urls import path

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    # email_confiramtion
    path('email_required/',views.TemplateView.as_view(template_name='account/email_confirmation_required.html'),name='required'),
    path('email_confirmation/'views.TemplateView.as_view(template_name='account/email_confirmation_done.html'),name='done'),
    
    # zokbo
    path('zokbo/<int:pk>/',views.DetailZokboView.as_view(),name='detail'),
    path('zokbo_upoload/',views.CreateZokboView.as_view(),name ='create'),
    path('zokbo/<int:pk>/update,views.UpdateZokboView.as_view(),name='update'),
    path('zokbo/<int:pk>/delete,views.DeleteZokboView.as_view(),name='delete'),
         
    # profile
    path('profile/<int:user_id>/',views.ProfileView.as_view(),name= 'profile'),
    path('profile/<int:user_id>/reviews/',views.UserReviewListView.as_view(),name='user-review-list'),
    path('profile-set/',views.ProfileSetView.as_view(),name= 'profile-set'),
    path('edit-profilet',views.ProfileUpdateView.as_view(),name='profile-update')
]
