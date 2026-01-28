from django.urls import path
from users.views import sign_in,sign_out,sign_up,activate_user,admin_dashboard,assign_role

urlpatterns = [
    path('signup/', sign_up, name='signup'),
    path('signin/', sign_in, name='signin'),
    path('signout/', sign_out, name='signout'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path('admin/dashboard',admin_dashboard,name='admin-dashboard'),
    path('admin/<int:user_id/assign-role/',assign_role,name='assign-role')
]
