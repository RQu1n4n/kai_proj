from django.shortcuts import render

# Create your views here.
from serpapi import GoogleSearch
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        
    
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    params = {
    "api_key": "a88eda312e3c45af4a84767846dd8bb81b488550e47d93346b5c8525fdf77ce2",
    "engine": "google_scholar_profiles",
    "mauthors":  request.user.profile ,
}

    search = GoogleSearch(params)
    results = search.get_dict()
    profiles_json =json.dumps(results["profiles"])
    profiles = json.loads(profiles_json)

    #    return render(request, self.template_name, {'profiles': profiles})

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profiles': profiles,
    }

    return render(request, 'users/profile.html', context)
