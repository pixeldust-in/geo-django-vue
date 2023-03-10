from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse


# Create your views here.
def root(request):
    return redirect(reverse("home"))


@login_required
def home(request):
    return render(request, "app.html")


def notfoundview(request):
    return HttpResponseNotFound("Page Not found!")
