from django.urls import path
from users.views import SignInView,SignUpView,SignOutView,ActivateUserView,AdminDashboardView,AssignRoleView,ParticipantListView,CreateGroupView,GroupListView,ProfileView,EditProfileView,ChangePasswordView,no_permission_view
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', SignOutView.as_view(), name='signout'),

    path('activate/<int:user_id>/<str:token>/', ActivateUserView.as_view()),

    path('admin/dashboard', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', AssignRoleView.as_view(), name='assign-role'),
    path('admin/create_group', CreateGroupView.as_view(), name='create-group'),
    path('admin/group-list', GroupListView.as_view(), name='group-list'),
    path('admin/participants/', ParticipantListView.as_view(), name='participant-list'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('no-permission/', no_permission_view, name='no-permission'),
]