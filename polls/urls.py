
from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('polls/<int:poll_id>/', views.detail, name='detail'),
    path('polls/results/', views.results, name='results'),
    path('results/<int:poll_id>/', views.results, name='results'),
    path('polls/<int:poll_id>/vote/', views.vote, name='vote'),
    path('polls/create/', views.create_poll, name='create_poll'),
    path('polls/signup/', views.signup, name='signup'),
    path('polls/login/', views.user_login, name='login'),
    path('polls/logout/', views.user_logout, name='logout'),
]