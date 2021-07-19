from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def test(request: HttpRequest):
    return render(request, "menu.html", {"showmenu": True})