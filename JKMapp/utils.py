import qrcode

# genrate qr code function 
from PIL import Image, ImageDraw, ImageFont
import datetime
import os

def generate_multiple_qr_codes(num_qr):
    qr_codes = []
    for i in range(1, num_qr+1):
        qr = qrcode.QRCode(
            version=1,
            box_size=5,
            border=4,
        )
        qr_data = f'JKM2024_{i}'
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_codes.append(qr_img)
    return qr_codes


def combine_qr_codes(qr_codes, margin=10):
    qr_width = qr_codes[0].size[0]
    qr_height = qr_codes[0].size[1]
    total_width = qr_width
    total_height = len(qr_codes) * qr_height + (len(qr_codes) - 1) * margin
    combined_image = Image.new('RGB', (total_width, total_height), color='white')
    y_offset = 0
    for qr in qr_codes:
        combined_image.paste(qr, (0, y_offset))
        y_offset += qr_height + margin
    return combined_image


def create_canvas(number, ticket_template, margin =10):
    ticket_width, ticket_height = ticket_template.size

    # Calculate total dimensions for combined image
    total_width = ticket_width

    total_height = (int(number) * ticket_height) +  margin

    # Create a new image with dimensions for combined tickets
    ticket_canvas = Image.new('RGB', (total_width, total_height), color='white')
    return ticket_canvas

def generate_qr_codes(num_qr=1, data_prefix="JKM2024"):
    qr_codes = []
    for i in range(1, num_qr+1):
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4,
        )
        qr_data = f'{data_prefix}_{i}'
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_codes.append(qr_img)
    return qr_codes


def put_tickets(canvas, number, qr_codes, ticket_template, margin=10):
        # Paste each QR code on a ticket layout
        y_offset = 0
        ticket_width, ticket_height = ticket_template.size

        for qr in qr_codes:
            # Paste ticket layout on combined image
            canvas.paste(ticket_template, (0, y_offset))
            y_offset += ticket_height + margin

        return canvas


def putqr(canvas, qr_codes, ticket_template ,margin = 10):
    y_offset = 0
    ticket_width, ticket_height = ticket_template.size
    qr_width, qr_height = qr_codes[0].size
    for qr in qr_codes:
        # Paste QR code on ticket layout
        qr_x_offset = ticket_width - qr_width - margin
        qr_y_offset = y_offset + (ticket_height - qr_height) // 2
        canvas.paste(qr, (qr_x_offset, qr_y_offset))
        y_offset += ticket_height + margin
    return canvas

def add_text_to_image(canvas, number, ticket_template, text_info, font_path, font_size, color, margin=10):

    ticket_width, ticket_height = ticket_template.size

    # Create a draw object.
    draw = ImageDraw.Draw(canvas)

    # Create a font object.
    font = ImageFont.truetype(font_path, size=font_size)

    # Draw the text on the new image.
    for a in range(number):
        for text, position in text_info:
            draw.text((position[0], position[1] + ((ticket_height)+margin)*a ), text, fill=color, font=font)
            
            # Adjust y_offset for next text line

  # Adjust y_offset for next ticket

    # Return the new image with the text added.
    return canvas



def create_tickets(number, ticket_template, margin =10, data_prefix="JKM2024", font_path = "JKMapp/static/KodeMono-Regular.ttf"):
    # 1. Define prerequisites and variables
    #font_path = "KodeMono-Regular.ttf"
    font_size = 50
    color = (255, 0, 0)
    text_info = []

    # Get current date and time
    current_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_date = current_datetime.strftime("%d-%m-%Y")
    formatted_time = current_datetime.strftime("%H:%M:%S")
    ticket_number = "www.JKMevents.in"


    # Populate text information
    text_info.append((f"{formatted_date}", (250, 800)))
    text_info.append((f"{formatted_time}", (250, 880)))
    text_info.append(("Rs.100", (250, 970)))
    text_info.append((f"{ticket_number}", (250, 1050)))


    # 2. Make a copy of the ticket template
    ticket_template_copy = ticket_template.copy()


    # 3. Run the first loop to paste text information
    draw = ImageDraw.Draw(ticket_template_copy)
    font = ImageFont.truetype(font_path, size=font_size)
    for text, position in text_info:
        draw.text(position, text, fill=color, font=font)

    # 4. Create the canvas
    ticket_width, ticket_height = ticket_template_copy.size
    total_width = ticket_width
    total_height = number * (ticket_height + margin)
    canvas = Image.new('RGB', (total_width, total_height), color='white')
    
    
    y_offset = 0
    
    for i in range(1, number + 1):
        qr = qrcode.QRCode(
            version=1,
            box_size=15,
            border=4,
            )
        qr_data = f'{data_prefix}_{i}'
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # 6. Paste the QR code onto the ticket template copy    
        qr_width, qr_height = qr_img.size
        qr_x_offset = ticket_width//2 - qr_width//2
        qr_y_offset = y_offset + int(ticket_height*2/3)
        ticket_template_copy.paste(qr_img, (qr_x_offset, qr_y_offset))
        # 7. Paste the ticket template copy onto the canvas
        canvas.paste(ticket_template_copy, (0, (ticket_height + margin) * (i - 1)))

     # 8. Return the canvas
    return canvas
