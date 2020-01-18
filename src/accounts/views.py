from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages
from to_do.models import ToDo
from django.db.models import Count


class SignUpView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = forms.UserCreateForm
    success_url="/accounts/login/"


def profile_detail_view(request, slug):

    profile = get_object_or_404(UserProfile, slug=slug)

    template_name = 'profile/profile.html'
    to_do_done = ToDo.objects.filter(user=request.user , status=True)
    to_do_not_yet = ToDo.objects.filter(user= request.user , status=False)

    context ={
        'userprofile':profile,
        'to_do_done':to_do_done,
        "to_do_not_yet":to_do_not_yet}
    return render(request, template_name, context)



@login_required
def update_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    user = get_object_or_404(User, username=request.user.username)

    if request.method == "POST":
        profile_form = forms.UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = forms.UserForm(request.POST, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('profile:detail', slug=request.user.username)
        else :
            messages.info(request, 'sorry something wrong Plz try again')
            return redirect('profile:edit')

    else:
        profile_form = forms.UserProfileForm(instance=profile)
        user_form = forms.UserForm(instance=user)

    template_name = 'profile/update_profile.html'

    context ={'profile_form':profile_form,'user_form':user_form ,"profile": profile}
    return render(request,template_name, context)
