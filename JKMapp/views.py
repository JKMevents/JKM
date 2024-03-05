from django.shortcuts import render, HttpResponse, redirect
from .utils import create_tickets
import os
from django.views.decorators.csrf import csrf_protect
from PIL import Image
import datetime
from .models import TicketInformation
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
        

        # get the latest iteration number from the databse
        latest_iteration = TicketInformation.objects.latest('id').iteration if TicketInformation.objects.exists() else 0

        # SAVE ticket information to the database
        current_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
        ticket_info = TicketInformation.objects.create(
            iteration = latest_iteration +1, 
            ticket_count = num,
            date = current_datetime.date(),
            time = current_datetime.time()
        )
        ticket_info.save()
        
        return redirect('counter')


    total_tickets = TicketInformation.objects.aggregate(Sum('ticket_count'))['ticket_count__sum']

    # Pass the total_tickets to the context
    context = {
        'total_tickets': 0,
        #'csrf_token': request.POST.get('csrfmiddlewaretoken')
    }


    return render(request, "counter.html", context)




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
