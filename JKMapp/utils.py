import qrcode
from PIL import Image
# genrate qr code function 

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
