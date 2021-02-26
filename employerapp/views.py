from django.shortcuts import render


def employer_cabinet(request):
    title = 'Личный кабинет работодателя'
    context = {'title': title}
    return render(request, 'employerapp/employer_cabinet.html', context)
