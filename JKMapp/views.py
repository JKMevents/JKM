from django.shortcuts import render, HttpResponse, redirect
from .utils import create_tickets
import os
from django.views.decorators.csrf import csrf_protect
from PIL import Image
import datetime
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
        margin = 10
        dir = "JKMapp/static/qrcode/"
        os.makedirs(dir, exist_ok=True)
        
        # Redirect to the same view after processing the form submission
        font_path = "JKMapp/static/KodeMono-Regular.ttf"
        num = int(num)

        ticket_template_dir = "JKMapp/static/Ticket_template.png" 
        ticket_template = Image.open(ticket_template_dir)       
        canvas = create_tickets(num, ticket_template, margin =10, data_prefix="JKM2024",font_path=font_path)

        os.makedirs(dir, exist_ok=True)
        canvas.save(os.path.join(dir, "tickets.png"))
        return redirect('counter')

    return render(request, "counter.html")




def test(request):
    if request.method == "POST":
        num = request.POST.get('display')
        if int(num) == 0:
            # Include the CSRF token when rendering the template
            return render(request, "test.html", {'csrf_token': request.POST.get('csrfmiddlewaretoken')})
        dir = "JKMapp/static/qrcode/"
        os.makedirs(dir, exist_ok=True)
        return redirect('test')


    return render(
        request,
        "test.html"
    )
