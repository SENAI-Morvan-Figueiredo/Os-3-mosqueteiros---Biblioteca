from django.shortcuts import render, redirect, HttpResponse

def teste(request):
    return HttpResponse("tela adm! - a partir do app")