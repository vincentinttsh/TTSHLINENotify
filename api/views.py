from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
import requests
from TTSHLINENotify import settings
from .models import AccessToken
import logging

logger = logging.getLogger(__name__)

def index(request):
    if request.session.get('registered', False):
        return render(request, "register.html")
    return render(request, "register.html", {
        "id": settings.LINE_CLIENT,
        "url": settings.HOST+"/register",
    })


def register(request):
    if not request.GET.get("code", False):
        return HttpResponseForbidden("Not for you")
    payload, url = {
        "grant_type": "authorization_code",
        "code": request.GET.get("code"),
        "redirect_uri": settings.HOST+"/register",
        "client_id": settings.LINE_CLIENT,
        "client_secret": settings.LINE_CLIENT_KEY
    }, "https://notify-bot.line.me/oauth/token"
    r = requests.post(url, params=payload)
    if r.status_code == 200:
        token = r.json()["access_token"]
        url = "https://notify-api.line.me/api/status"
        headers = {
            "Authorization": "Bearer " + token,
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            data = r.json()
            AccessToken(
                token=token,
                userType=data["targetType"],
                username=data["target"],
            ).save()
        else:
            AccessToken(
                token=token,
            ).save()
        request.session["registered"] = True
        return HttpResponseRedirect("/")
    else:
        return HttpResponseForbidden("Fail")
