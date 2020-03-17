from django.shortcuts import render
import requests
from subprocess import run,PIPE
import sys

def button(request):

    return render(request,'home.html')

def output(request):
    data=requests.get("https://www.google.com/")
    print(data.text)
    data=data.text
    return render(request,'home.html',{'data':data})

def external(request):
    inp=request.POST.get('param')
    out=run([sys.executable,"C:\\Users\\hp\\Desktop\\Python Scripts\\test.py",inp],shell=False,stdout=PIPE)
    o=out.stdout
    print(o)

    return render(request,'home.html',{'data1':o})
