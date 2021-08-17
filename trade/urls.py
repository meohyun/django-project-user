from . import views
from django.urls import path

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('zokbo/<int:pk>/',views.DetailZokboView.as_view(),name='detail'),
    path('zokbo_upoload/',views.CreateZokboView.as_view(),name ='create'),
    path('zokbo/<int:pk>/update,views.UpdateZokboView.as_view(),name='update'),
    path('zokbo/<int:pk>/delete,views.DeleteZokboView.as_view(),name='delete')     
     
]
