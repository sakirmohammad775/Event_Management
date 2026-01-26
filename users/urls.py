from django.urls import path
from users.views import sign_in,sign_out,sign_up

urlpatterns = [
    path('signup/', sign_up, name='signup'),
    path('signin/', sign_in, name='signin'),
    path('signout/', sign_out, name='signout'),
]
