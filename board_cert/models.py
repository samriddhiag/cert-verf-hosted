from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from upload_data.models import FontStyle
#from .utils import unique_slug_generator

import string 
from django.utils.text import slugify 
import random 

# Create your models here.


class Board_Certificate(models.Model):
    Designation = models.TextField(default=None)
    image = models.ImageField(upload_to='certificates/')
    text_color_R = models.IntegerField(default=0)
    text_color_G = models.IntegerField(default=0)
    text_color_B = models.IntegerField(default=0)
    font_size = models.IntegerField(default=2)
    font_type = models.ForeignKey(to=FontStyle, on_delete=models.PROTECT, related_name="fontType")
    board_name_location_x = models.IntegerField(default=2)
    board_name_location_y = models.IntegerField(default=2)
    boardposition_name_location_x = models.IntegerField(default=2)
    boardposition_name_location_y = models.IntegerField(default=2)
    qr_code_location_x = models.IntegerField(default=2)
    qr_code_location_y = models.IntegerField(default=2)
    qr_code_size_x = models.IntegerField(default=2)
    qr_code_size_y = models.IntegerField(default=2)
    def __str__(self):
        return str(self.Designation)


class Board_member_details(models.Model):
    Board_Full_Name = models.TextField(max_length=50) 
    Designation = models.ForeignKey(to=Board_Certificate, on_delete=models.PROTECT, related_name="eventsname")
    Description_n_about = models.TextField()
    Photo = models.ImageField(upload_to='board_photos', blank = True)
    facebook_link = models.TextField(max_length=250, default="")
    linkedin_link = models.TextField(max_length=250, default="")
    github_link = models.TextField(max_length=250, default="")
    slug = models.SlugField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.Board_Full_Name)

def random_string_generator_b(size = 10, chars = string.ascii_lowercase + string.digits): 
        return ''.join(random.choice(chars) for _ in range(size)) 
  
def unique_slug_generator_b(instance, new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(instance.Board_Full_Name) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists() 
        
    if qs_exists: 
        new_slug = "{randstr}".format( 
            slug = slug, randstr = random_string_generator_b(size = 8)) 
               
        return unique_slug_generator_b(instance, new_slug = new_slug) 
    return "{randstr}".format(slug = slug, randstr = random_string_generator_b(size = 8)) 
    
def pre_save_receiver_b(sender, instance, *args, **kwargs): 
    if not instance.slug: 
        instance.slug = unique_slug_generator_b(instance)

pre_save.connect(pre_save_receiver_b, sender = Board_member_details) 