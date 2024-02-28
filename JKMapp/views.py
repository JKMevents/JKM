from django.shortcuts import render, HttpResponse, redirect
from .utils import generate_multiple_qr_codes, combine_qr_codes, create_canvas, generate_qr_codes, put_tickets, putqr, add_text_to_image
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
        qrcodes = generate_multiple_qr_codes(int(num))
        margin = 10
        tickets = combine_qr_codes(qrcodes, margin)
        dir = "JKMapp/static/qrcode/"
        os.makedirs(dir, exist_ok=True)
        tickets.save(os.path.join(dir, "tickets.png"))
        
        # Redirect to the same view after processing the form submission
        font_path = "JKMapp/static/KodeMono-Regular.ttf"

        font_size = 50
        color = (255, 0, 0)

        # Get current date and time
        current_datetime = datetime.datetime.now()

        # Format the datetime object as a string
        formatted_date = current_datetime.strftime("%d-%m-%Y")
        formatted_time = current_datetime.strftime("%H:%M:%S")
        ticket_number = "www.JKMevents.in"

        # Define text and positions
        text_info = [
            (f"{formatted_date}", (200, 350)),
            (f"{formatted_time}", (700, 470)),
            ("Rs.100", (1250, 470)),
            (f"{ticket_number}", (1550, 470))
        ]
        num = int(num)
        
        ticket_template_dir = "JKMapp/static/Ticket.png"        
        ticket_template = Image.open(ticket_template_dir)
        canvas = create_canvas(num, ticket_template, margin =10)
        qr_codes = generate_qr_codes(num, data_prefix="JKM2024")
        ticket_canvas = put_tickets(canvas, num, qr_codes, ticket_template, margin=10)
        ticket_qr_canvas = putqr(canvas, qr_codes, ticket_template ,margin = 10)
        ticket_result = add_text_to_image(canvas, num, ticket_template, text_info, font_path, font_size, color, margin=10)
        dir = "JKMapp/static/qrcode/"
        os.makedirs(dir, exist_ok=True)
        ticket_result.save(os.path.join(dir, "tickets.png"))
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
