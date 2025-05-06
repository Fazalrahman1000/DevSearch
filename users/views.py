from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Profile, Skills
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm , ProfileForm
from django.contrib.auth.models import User
# Create your views here.


def loginUser(request):
    page = 'login'
    context = {'page':page}
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'user not exist!')
        user = authenticate(request, username = username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "invalid username or password")

    return render(request, 'users/login-register.html', context)


def logoutUser(request):
    logout(request)
    messages.success(request, 'User is logged out!')
    return redirect('login')


def registerUser(request):
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user but don't commit yet (to modify username)
            user = form.save(commit=False)
            user.username = user.username.lower()  # Make sure username is lowercase
            user.save()  # Save the user

            # Log the user in after successful registration
            login(request, user)
            
            # Show success message
            messages.success(request, "User Created Successfully!")
            return redirect('profiles')  # Redirect to the profiles page after successful registration
        else:
            # Handle form errors (e.g., validation errors)
            messages.error(request, "There was an error with your registration.")

    page = 'register'
    context = {'page': page, 'form': form}
    return render(request, 'users/login-register.html', context)



def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skills_set.exclude(description__exact="")
    otherSkills = profile.skills_set.filter(description="")
    context = {'profile':profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skills_set.all()
    projects = profile.projects_set.all()
    context = {"profile":profile, 'skills':skills,'projects':projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance = profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance = profile)
        if form.is_valid():
            form.save()
            return redirect('account')
        
    context={'form':form}
    return render(request, 'users/profile_form.html', context)