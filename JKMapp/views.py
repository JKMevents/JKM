from django.shortcuts import render, HttpResponse, redirect
from .utils import create_tickets, read_counters, update_counters, generate_pdf_from_excel, BarcodeReader, check_and_save_string
import os
from django.views.decorators.csrf import csrf_protect
from PIL import Image
import datetime




from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile





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
COUNTERS_PDF_FILE_PATH = 'JKMapp/static/counter_info.pdf'


@csrf_protect
def counter(request):
    total_count = read_counters()
    start_number = total_count
    if request.method == "POST":
        num = request.POST.get('display')
        num = int(num)
        if num == 0:
            # Include the CSRF token when rendering the template
            return render(request, "counter.html", {'csrf_token': request.POST.get('csrfmiddlewaretoken')})
        
        margin = 20
        os.makedirs(QR_CODE_DIR, exist_ok=True)
        
        ticket_template = Image.open(TICKET_TEMPLATE_DIR)       
        canvas = create_tickets(num, start_number , ticket_template, margin =margin, data_prefix="JKM2024",font_path=FONT_PATH)
        
        canvas.save(os.path.join(QR_CODE_DIR, "tickets.png"))
        
        # Update counter information
        
        total_count += 1
        ticket_count=0
        ticket_count += num
        update_counters(total_count, ticket_count)

        return redirect('counter')

    info = {"total_tickets": total_count}
    return render(request, "counter.html", info)




@csrf_protect
def test(request):
        if request.method == 'POST':
        # Get the path to the Excel file
            input_excel = COUNTERS_FILE_PATH  # Replace with the actual path to your Excel file

        # Generate a unique filename for the PDF
            output_pdf = COUNTERS_PDF_FILE_PATH
            generate_pdf_from_excel(input_excel, output_pdf)
        return render(
        request,
        "test.html"
        )

@csrf_protect
def upload_image(request):
    if request.method == 'POST':
        data = request.POST.get('image_data')
        print('Received data:', data)  # Debugging statement

        if data:
            try:
                format, imgstr = data.split(';base64,')
                ext = format.split('/')[-1]

                # Convert base64 data to a file object
                img_data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

                # Process the image data as needed (e.g., save to disk, perform further processing)
                # Replace this with your actual processing logic

                print('Image uploaded successfully')  # Debugging statement
                return JsonResponse({'message': 'Image uploaded successfully'})
            except Exception as e:
                print('Error processing image:', e)  # Debugging statement
        else:
            print('No image data received')  # Debugging statement
    else:
        print('Invalid request method')  # Debugging statement


    
    
    return render(
        request,
        "cam.html"
        )



import cv2

def scanner(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        # Define the directory where you want to save the uploaded images
        upload_dir = 'JKMapp/static/images/'
        # Ensure the upload directory exists
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Construct the file path to save the uploaded image
        file_path = os.path.join(upload_dir, image_file.name)

        # Save the uploaded image to the file path
        with open(file_path, 'wb') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        barcodedata = BarcodeReader(file_path)

        check_and_save_string(barcodedata, "JKMapp/static/paytm.csv")
        #print(barcodedata)
        
        #return HttpResponse('Image uploaded successfully.')
    else:
        print("did not get any image")
    return render(request, 'scanner.html')










