from django.shortcuts import render
from django.http import HttpResponse

def lista_vr(request):
    # Aquí puedes consultar los modelos VR y pasarlos al template
    return render(request, 'VirtualR/lista.html')

def prueba(request):
    return HttpResponse("¡Hola desde VirtualR!")
