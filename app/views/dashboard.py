from django.shortcuts import render
from rest_framework.views import APIView

def dashboard_view(request):
    return render(request, "base.html")

