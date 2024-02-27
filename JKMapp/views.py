from django.shortcuts import render, HttpResponse
from .utils import generate_multiple_qr_codes, combine_qr_codes
import os
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def Home(request):
    return render(
        request,
        "home.html"
    )


def signup_client(request):
    return render(request, HttpResponse("Signup for clinet"))

def login_client(request):
    return render(request, HttpResponse("login for client"))

def signup_customer(request):
    return render(request, HttpResponse("Sign up for customer"))

def login_customer(request):
    return render(request, HttpResponse("login for customer"))




@csrf_protect
def counter(request):
    if request.method == "POST":
        num = request.POST.get('display')
        if int(num) == 0:
            # Include the CSRF token when rendering the template
            return render(request, "counter.html", {'csrf_token': request.POST.get('csrfmiddlewaretoken')})
        qrcodes = generate_multiple_qr_codes(int(num))
        margin = 10
        tickets = combine_qr_codes(qrcodes, margin)
        dir = "JKMapp/static/qrcode/"
        os.makedirs(dir, exist_ok=True)
        tickets.save(os.path.join(dir, "tickets.png"))
        print('code is working')
        # Redirect to the same view after processing the form submission
        return redirect('counter')

    return render(request, "counter.html")




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
