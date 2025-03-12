from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import UserProfile
from app.forms import UserProfileForm

@login_required
def update_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after updating
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, "profile_update.html", {"form": form})
