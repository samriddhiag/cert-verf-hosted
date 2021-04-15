from django.shortcuts import render
from board_cert.models import Board_member_details, Board_Certificate, FontStyle
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
from django.http import HttpResponse, FileResponse
import img2pdf
import pyqrcode 
# Create your views here.

def generate_board_certificate(request, slug):
    if request.method=='GET':
        board_data = Board_member_details.objects.get(slug=slug)
        board_certificate_data = Board_Certificate.objects.get(id=board_data.Designation_id)
        im = Image.open(board_certificate_data.image)
        d = ImageDraw.Draw(im)
        board_name_location = (board_certificate_data.board_name_location_x, board_certificate_data.board_name_location_y)
        designation_name_location = (board_certificate_data.boardposition_name_location_x, board_certificate_data.boardposition_name_location_y)
        text_color = (board_certificate_data.text_color_R, board_certificate_data.text_color_G, board_certificate_data.text_color_B)
        font_style = FontStyle.objects.get(id=board_certificate_data.font_type_id)
        font = ImageFont.truetype("get_board_data/arial.ttf", board_certificate_data.font_size)
        d.text(board_name_location, board_data.Board_Full_Name, fill=text_color, font=font)
        d.text(designation_name_location, board_certificate_data.Designation, fill=text_color, font=font)
        url = pyqrcode.QRCode("https://ieee-cs-cert-verify.herokuapp.com/board/"+str(slug))
        url.png('test.png', scale=1)
        qr = Image.open('test.png')
        qr = qr.resize((board_certificate_data.qr_code_size_x, board_certificate_data.qr_code_size_y))
        qr = qr.convert("RGBA")
        im = im.convert("RGBA")
        box = (board_certificate_data.qr_code_location_x, board_certificate_data.qr_code_location_y)
        #qr.crop(box)
        #region = im
        print(im)
        print(qr)
        im.paste(qr, box) 
        #im.show()
        response = HttpResponse(content_type='image/png')
        im.save(response, "PNG")
        return response

def convert_certificate_to_pdf(request, slug):
     if request.method=='GET':
        user_data = Board_member_details.objects.get(slug=slug)
    
        #print(user_data.Full_Name)
        #print(user_data.Event_Name)
        certificate_data = Board_Certificate.objects.get(id=user_data.Designation_id)
        #print(certificate_data.image)
        im = Image.open(certificate_data.image)
        d = ImageDraw.Draw(im)
        participate_name_location = (certificate_data.board_name_location_x, certificate_data.board_name_location_y)
        event_name_location = (certificate_data.boardposition_name_location_x, certificate_data.boardposition_name_location_y)
        text_color = (certificate_data.text_color_R, certificate_data.text_color_G, certificate_data.text_color_B)
        font_style = FontStyle.objects.get(id=certificate_data.font_type_id)
        font = ImageFont.truetype("get_board_data/arial.ttf", certificate_data.font_size)
        d.text(participate_name_location, user_data.Board_Full_Name, fill=text_color, font=font)
        d.text(event_name_location, certificate_data.Designation, fill=text_color, font=font)
        url = pyqrcode.QRCode("https://ieee-cs-cert-verify.herokuapp.com/board/"+str(slug))
        url.png('test.png', scale=1)
        qr = Image.open('test.png')
        qr = qr.resize((certificate_data.qr_code_size_x, certificate_data.qr_code_size_y))
        qr = qr.convert("RGBA")
        im = im.convert("RGBA")
        box = (certificate_data.qr_code_location_x, certificate_data.qr_code_location_y)
        #qr.crop(box)
        #region = im
        print(im)
        print(qr)
        im.paste(qr, box)
        Imgfile = im.convert("RGB")
        #pdf_bytes = img2pdf.convert(im)
        #print(pdf_bytes)
        #response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'inline; filename=' + str(user_data.Full_Name) + '.pdf'
        
        img_bytes = BytesIO()
        Imgfile.save(img_bytes, "PDF")
        img_bytes = img_bytes.getvalue()
        #print(img_bytes)
        response = HttpResponse(img_bytes , content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + str(user_data.Board_Full_Name) + '.pdf'
        #response = FileResponse(img_bytes) 
        return response


def display_board_certificate(request, slug):
    if request.method=='GET':
        board_data = Board_member_details.objects.get(slug=slug)
        board_certificate_data = Board_Certificate.objects.get(id=board_data.Designation_id)
        print(board_data.Photo)
        return render(request, 'view_certificate_board.html', {"slug":slug, "first_name": board_data.Board_Full_Name, "designation": board_data.Designation,
                                                                "description": board_data.Description_n_about, "board_profile_image": board_data.Photo,
                                                                'facebook_link': board_data.facebook_link, 'linkedin_link': board_data.linkedin_link, 'github_link': board_data.github_link})


def board_profile_image(request, slug):
    if request.method=='GET':
        board_data = Board_member_details.objects.get(slug=slug)
        profile_image = board_data.Photo
        response = HttpResponse(profile_image, content_type='image/png')
        return response