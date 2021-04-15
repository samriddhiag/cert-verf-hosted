from django.shortcuts import render
from upload_data.models import ParticipantData, Certificate, FontStyle
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
from django.http import HttpResponse, FileResponse
import img2pdf
import pyqrcode
import environ

# Create your views here.


###### This function generate certificate as image and send that image as response i.e this is API based route can be used on multi platform
def generate_certificate(request, slug):
    if request.method=='GET':
        user_data = ParticipantData.objects.get(slug=slug)  # get specific user data from database using primary key "slug"
        certificate_data = Certificate.objects.get(id=user_data.Event_Name_id) # get certificate data from database using Event id (FK) where FK = foreign key

        im = Image.open(certificate_data.image) # open image 
        d = ImageDraw.Draw(im) # code to give edit access to image selected 
        participate_name_location = (certificate_data.participate_name_position_x, certificate_data.participate_name_position_y) # give location in terms of co-ordinate for participant name in certificate  
        event_name_location = (certificate_data.event_name_position_x, certificate_data.event_name_position_y) # give location for even name in certificate (co-ordinates is used)
        text_color = (certificate_data.text_color_R, certificate_data.text_color_G, certificate_data.text_color_B) # set color
        font_style = FontStyle.objects.get(id=certificate_data.font_type_id)
        #print(font_style.font_type)
        
        font = ImageFont.truetype("get_data/arial.ttf", certificate_data.font_size) # set font size
         
        ######## write text i.e full name, event name  into certificate
        d.text(participate_name_location, user_data.Full_Name, fill=text_color, font=font) 
        d.text(event_name_location, certificate_data.Event_Name, fill=text_color, font=font)
        ########
        

        url = pyqrcode.QRCode("https://ieee-cs-cert-verify.herokuapp.com/events/"+str(slug)) # set dyanmic URL link into qr code 
        url.png('test.png', scale=1)
        qr = Image.open('test.png')
        qr = qr.resize((certificate_data.qr_code_size_x, certificate_data.qr_code_size_y)) # set QR code position
        # convert to pdf
        qr = qr.convert("RGBA")
        im = im.convert("RGBA")
        box = (certificate_data.qr_code_position_x, certificate_data.qr_code_position_y)
        im.paste(qr, box) # pasted qr code into certificate 
        response = HttpResponse(content_type='image/png')  # send as response
        im.save(response, "PNG")
        return response

########


####### This function convert Image to pdf and send that PDF as response i.e this is API based route can be used on multi platform
def convert_certificate_to_pdf(request, slug):
     if request.method=='GET':
        user_data = ParticipantData.objects.get(slug=slug)
        certificate_data = Certificate.objects.get(id=user_data.Event_Name_id)
        im = Image.open(certificate_data.image)
        d = ImageDraw.Draw(im)
        participate_name_location = (certificate_data.participate_name_position_x, certificate_data.participate_name_position_y)
        event_name_location = (certificate_data.event_name_position_x, certificate_data.event_name_position_y)
        text_color = (certificate_data.text_color_R, certificate_data.text_color_G, certificate_data.text_color_B)
        font_style = FontStyle.objects.get(id=certificate_data.font_type_id)
        #print(font_style.font_type)
        font = ImageFont.truetype("get_data/arial.ttf", certificate_data.font_size) # set font size
        d.text(participate_name_location, user_data.Full_Name, fill=text_color, font=font)
        d.text(event_name_location, certificate_data.Event_Name, fill=text_color, font=font)
        url = pyqrcode.QRCode("https://ieee-cs-cert-verify.herokuapp.com/events/"+str(slug))
        url.png('test.png', scale=1)
        qr = Image.open('test.png')
        qr = qr.resize((certificate_data.qr_code_size_x, certificate_data.qr_code_size_y))
        qr = qr.convert("RGBA")
        im = im.convert("RGBA")
        box = (certificate_data.qr_code_position_x, certificate_data.qr_code_position_y)
        im.paste(qr, box)
        Imgfile = im.convert("RGB")
        img_bytes = BytesIO()
        Imgfile.save(img_bytes, "PDF")
        img_bytes = img_bytes.getvalue()
        response = HttpResponse(img_bytes , content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + str(user_data.Full_Name) + '.pdf'
        return response
#######


##### This function render view_certificate.html by taking arguments as request (here get request) and slug from URL
def display_certificate(request, slug):
    if request.method=='GET':
        user_data = ParticipantData.objects.get(slug=slug)
        certificate_data = Certificate.objects.get(id=user_data.Event_Name_id)
        return render(request, 'view_certificate.html', {"slug":slug, "description": user_data.Description, "name": user_data.Full_Name, 
        "local_certificate_route": "http://127.0.0.1:8000/generate_certificate/"+str(slug),
        "hosted_certificate_route": "https://ieee-cs-cert-verify.herokuapp.com/generate_certificate/"+str(slug)})
#######
