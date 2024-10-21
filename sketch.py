from PIL import Image
import qrcode

qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
)
qr.add_data('some kind of text')
img: Image = qr.make_image(fill="black", back_color="white").convert('RGB')

img = img.resize((500, 500), Image.Resampling.LANCZOS)
bg: Image = Image.open('./bg.jpg').convert("RGBA")

img_w, img_h = img.size
bg_w, bg_h = bg.size

offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)

bg.paste(img, offset)

bg.save('out.png')
