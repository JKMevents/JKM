from django.shortcuts import render, HttpResponse, redirect
from .utils import create_tickets, read_counters, update_counters
import os
from django.views.decorators.csrf import csrf_protect
from PIL import Image
import datetime
from django.db.models import Sum


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


COUNTERS_FILE_PATH = 'JKMapp/static/counter_info.xlsx'
QR_CODE_DIR = 'JKMapp/static/qrcode/'
FONT_PATH = 'JKMapp/static/Roboto-Medium.ttf'
TICKET_TEMPLATE_DIR = 'JKMapp/static/ticket_template_2.png'



@csrf_protect
def counter(request):
    total_count = read_counters()
    if request.method == "POST":
        num = request.POST.get('display')
        num = int(num)
        if num == 0:
            # Include the CSRF token when rendering the template
            return render(request, "counter.html", {'csrf_token': request.POST.get('csrfmiddlewaretoken')})
        
        margin = 20
        os.makedirs(QR_CODE_DIR, exist_ok=True)
        
        ticket_template = Image.open(TICKET_TEMPLATE_DIR)       
        canvas = create_tickets(num, ticket_template, margin =margin, data_prefix="JKM2024",font_path=FONT_PATH)
        
        canvas.save(os.path.join(QR_CODE_DIR, "tickets.png"))
        
        # Update counter information
        
        total_count += 1
        ticket_count=0
        ticket_count += num
        update_counters(total_count, ticket_count)

        return redirect('counter')

    info = {"total_tickets": total_count}
    return render(request, "counter.html", info)




def test(request):


    return render(
        request,
        "test.html"
    )
