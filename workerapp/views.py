from django.shortcuts import render


def worker_cabinet(request):
    title = 'Личный кабинет соискателя'
    context = {'title': title}
    return render(request, 'workerapp/worker_cabinet.html', context)
