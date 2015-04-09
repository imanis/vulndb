from django.shortcuts import render, redirect, get_object_or_404,\
    get_list_or_404


def home(request):
    return render(request, 'home/index.html')


def cantact(request):
    return render(request, 'home/contact.html')


def qualification(request):
    return render(request, 'home/index.html')


def jobs(request):
    return render(request, 'home/services.html')


def lnx(request):
    return render(request, 'home/KNX.html')


def company(request):
    return render(request, 'home/about.html')
