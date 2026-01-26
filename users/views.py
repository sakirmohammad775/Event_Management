from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import CustomRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator


# jbh234OINa!@
# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.is_active=False
            user.save() 
            messages.success(
                request, "A confirmation mail sent. Please check your email"
            )
            return redirect('signin')
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


def sign_out(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("home")

def activate_user(request,user_id,token):
    try:
        user=User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request, "Your account has been activated. You can now sign in.")
            return redirect('signin')
        else:
            return HttpResponse('Invalid Id or token')
    except User.DoesNotExist:
        return HttpResponse('User not found')