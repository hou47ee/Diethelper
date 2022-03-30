from account import views as v
from django.urls import path

urlpatterns = [
     path('home/', v.home_view, name='home'),
     path('register/', v.register_view, name='register'),
     path('login/', v.login_view, name='login'),
     path('logout/', v.logout_view, name='logout'),
     path('member/', v.member_view, name='member'),
     path('addata/', v.addata_view, name='addata'),
     path('history/', v.history_view, name='history'),
     path('deldata/', v.deldata_view, name= 'deldata'),
]