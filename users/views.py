from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from users.forms import CustomRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from users.forms import loginForm, AssignRoleForm, CreateGroupForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test

# jbh234OINa!@
# Create your views here.


def is_admin(user):
    return user.is_authenticated and user.groups.filter(name="Admin").exists()


def is_organizer(user):
    return user.is_authenticated and user.groups.filter(name="Organizer").exists()


def is_participant(user):
    return user.is_authenticated and user.groups.filter(name="Participant").exists()


def sign_up(request):
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.is_active = False
            user.save()

            # Automatically add the user to 'Participant' group
            try:
                participant_group = Group.objects.get(name="Participant")
                user.groups.add(participant_group)
            except Group.DoesNotExist:
                # Optional: create the group if it doesn't exist
                participant_group = Group.objects.create(name="Participant")
                user.groups.add(participant_group)
            messages.success(
                request, "A confirmation mail sent. Please check your email"
            )
            return redirect("signin")
    else:
        form = CustomRegistrationForm()
    return render(request, "users/signup.html", {"form": form})


## signin problem
def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("Doc", username, password)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "users/signin.html")


@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("home")


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request, "Your account has been activated. You can now sign in."
            )
            return redirect("signin")
        else:
            return HttpResponse("Invalid Id or token")
    except User.DoesNotExist:
        return HttpResponse("User not found")


@user_passes_test(is_admin, login_url="no-permission")
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, "admin/dashboard.html", {"users": users})


### Assign_role
@user_passes_test(is_admin, login_url="no-permission")
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get("role")
            user.groups.clear()
            user.groups.add(role)
            messages.success(
                request,
                f"User {user.username} has been assigned to the {role.name} role",
            )
            return redirect("admin-dashboard")
    return render(request, "admin/assign_role.html", {"form": form})


##create group
@user_passes_test(is_admin, login_url="no-permission")
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(
                request, f"Group {group.name} has been created successfully"
            )
            return redirect("create-group")
    return render(request, "admin/create_group.html", {"form": form})


## Group List
@user_passes_test(is_admin, login_url="no-permission")
def group_list(request):
    groups = Group.objects.all()
    return render(request, "admin/group_list.html", {"groups": groups})

def participant_list(request):
    try:
        participant_group = Group.objects.get(name="Participant")
        participants = participant_group.user_set.all()  # all users in this group
    except Group.DoesNotExist:
        participants = []

    return render(request, "admin/participant_list.html", {"participants": participants})