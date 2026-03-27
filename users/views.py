from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, FormView
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse

from users.forms import (
    CustomRegistrationForm,
    loginForm,
    AssignRoleForm,
    CreateGroupForm,
    EditProfileForm
)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

def no_permission_view(request):
    return render(request,'core/no_permission.html')  ###wait

##Role Check Mixins->
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name="Admin").exists()


class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Organizer").exists()


class ParticipantRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Participant").exists()
    

# SignUp
class SignUpView(View):
    def get(self, request):
        form = CustomRegistrationForm()
        return render(request, "users/signup.html", {"form": form})

    def post(self, request):
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            try:
                group = Group.objects.get(name="Participant")
            except Group.DoesNotExist:
                group = Group.objects.create(name="Participant")

            user.groups.add(group)

            messages.success(request, "A confirmation mail sent. Please check your email")
            return redirect("signin")

        return render(request, "users/signup.html", {"form": form})
    
##SIgnIn
class SignInView(View):
    def get(self, request):
        return render(request, "users/signin.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

        return render(request, "users/signin.html")
    
##SignOut
class SignOutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("home")
    
#ActivateUser
class ActivateUserView(View):
    def get(self, request, user_id, token):
        try:
            user = User.objects.get(id=user_id)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, "Your account has been activated. You can now sign in.")
                return redirect("signin")
            else:
                return HttpResponse("Invalid Id or token")

        except User.DoesNotExist:
            return HttpResponse("User not found")

## AdminDashboard
class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = "admin/admin_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        return context

## Assign Role
class AssignRoleView(AdminRequiredMixin, View):
    def get(self, request, user_id):
        form = AssignRoleForm()
        return render(request, "admin/assign_role.html", {"form": form})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = AssignRoleForm(request.POST)

        if form.is_valid():
            role = form.cleaned_data.get("role")
            user.groups.clear()
            user.groups.add(role)

            messages.success(request, f"User {user.username} assigned to {role.name}")
            return redirect("admin-dashboard")

        return render(request, "admin/assign_role.html", {"form": form})

##Create Group
class CreateGroupView(AdminRequiredMixin, View):
    def get(self, request):
        form = CreateGroupForm()
        return render(request, "admin/create_group.html", {"form": form})

    def post(self, request):
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} created successfully")
            return redirect("create-group")

        return render(request, "admin/create_group.html", {"form": form})

#Group List
class GroupListView(AdminRequiredMixin, ListView):
    model = Group
    template_name = "admin/group_list.html"
    context_object_name = "groups"
    
#Participant List
class ParticipantListView(View):
    def get(self, request):
        try:
            group = Group.objects.get(name="Participant")
            participants = group.user_set.all()
        except Group.DoesNotExist:
            participants = []

        return render(request, "admin/participant_list.html", {"participants": participants})

## Profile View
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile/profile.html"

## Edit Profile
class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)
        return render(request, "profile/edit_profile.html", {"form": form})

    def post(self, request):
        print("post request received")
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")

        return render(request, "profile/edit_profile.html", {"form": form})

#Change Password
class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, "profile/change_password.html", {"form": form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Password changed successfully.")
            return redirect("profile")

        return render(request, "profile/change_password.html", {"form": form})