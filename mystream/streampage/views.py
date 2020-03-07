from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import connection
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import UsersLoginForm, UsersRegisterForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.template.loader import render_to_string, get_template
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import json
import requests
import uuid
import hashlib
from datetime import datetime
from streampage.models import Primitives,communityUsers,Communities,Datatypes,DatatypeFields,Posts,CommunityTags,DatatTypeTags,PostTags,UserTags

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {})
    else:
        return HttpResponseRedirect("/streampage/login")
		
		
def login_view(request):
    form = UsersLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        login(request, user)
        return redirect("/streampage")
    return render(request, "login.html", {
		"form" : form,
		"title" : "Login",})


def register_view(request):
    form = UsersRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        comUsers = communityUsers()
        comUsers.userMail = user.email
        comUsers.nickName = user.username
        comUsers.save()
        new_user = authenticate(username = user.username, password = password)
        login(request, new_user)
        return redirect("/streampage/login")
    return render(request, "login.html", {
	    "title" : "Register",
	    "form" : form,
    })
 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/streampage/login")
	
