from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('profile', views.profile, name='profile'),
    path('signout', views.signout, name='signout'),
    path('registerCycle', views.registerCycle, name='registerCycle'),
    path('myCycleStatus', views.myCycleStatus, name='myCycleStatus'),
    path('requestCycle', views.requestCycle, name='requestCycle'),
    path('approveRequest', views.approveRequest, name='approveRequest'),
    path('rejectRequest', views.rejectRequest, name='rejectRequest'),
    path('makenotAvailable', views.makenotAvailable, name='makenotAvailable'),
    path('makeAvailable', views.makeAvailable, name='makeAvailable'),
    # # ex: /polls/
    # path('', views.index, name='index'),
    # # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]