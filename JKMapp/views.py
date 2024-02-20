from django.shortcuts import render
from .utils import generate_multiple_qr_codes, combine_qr_codes
import os
# Create your views here.
def Home(request):
    return render(
        request,
        "index.html"
    )

def counter(request):
    if request.method == "POST":
        num = request.POST.get('display')
        if int(num )==0:
            return render(request, "counter.html")
        qrcodes = []
        qrcodes = generate_multiple_qr_codes(int(num))
        margin = 10
        tickets =  combine_qr_codes(qrcodes, margin)
        dir = "JKMapp/static/qrcode/"
        os.makedirs(dir, exist_ok=True)
        tickets.save(dir + "tickets.png")
        print('code is working')


    return render(
        request,
        "counter.html"
    )

def test(request):
    if request.method == "POST":
        num = request.POST.get('display')
        if int(num )==0:
            return render(request, "counter.html")

        qrcodes = []
        qrcodes = generate_multiple_qr_codes(int(num))
        margin = 10
        tickets =  combine_qr_codes(qrcodes, margin)
        dir = "JKMapp/static/qrcode/"
        os.makedirs(dir, exist_ok=True)
        tickets.save(dir + "tickets" + num+ ".png")
        print('code is working')


    return render(
        request,
        "test.html"
    )
