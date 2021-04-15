from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify

#from .utils import unique_slug_generator

import string 
from django.utils.text import slugify 
import random 

# Create your models here.
class FontStyle(models.Model):
    font_type = models.TextField(default="aerial.ttf")
    def __str__(self):
        return str(self.font_type)

class Certificate(models.Model):
    Event_Name = models.TextField(max_length=50)
    image = models.ImageField(upload_to='certificates/')
    text_color_R = models.IntegerField(default=0)
    text_color_G = models.IntegerField(default=0)
    text_color_B = models.IntegerField(default=0)
    font_size = models.IntegerField(default=2)
    font_type = models.ForeignKey(to=FontStyle, on_delete=models.PROTECT, related_name="fonttype")
    participate_name_position_x = models.IntegerField(default=2)
    participate_name_position_y = models.IntegerField(default=2)
    event_name_position_x = models.IntegerField(default=2)
    event_name_position_y = models.IntegerField(default=2)
    qr_code_position_x = models.IntegerField(default=2)
    qr_code_position_y = models.IntegerField(default=2)
    qr_code_size_x = models.IntegerField(default=2)
    qr_code_size_y = models.IntegerField(default=2)
    def __str__(self):
        return str(self.Event_Name)


class ParticipantData(models.Model):
    Full_Name = models.TextField(max_length=50)
    Event_Name = models.ForeignKey(to=Certificate, on_delete=models.PROTECT, related_name="eventsname")
    Description = models.TextField(max_length=200)
    slug = models.SlugField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.Full_Name)







def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
        return ''.join(random.choice(chars) for _ in range(size)) 
  
def unique_slug_generator(instance, new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(instance.Full_Name) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists() 
        
    if qs_exists: 
        new_slug = "{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 8)) 
               
        return unique_slug_generator(instance, new_slug = new_slug) 
    return "{randstr}".format(slug = slug, randstr = random_string_generator(size = 8)) 
    
def pre_save_receiver(sender, instance, *args, **kwargs): 
    if not instance.slug: 
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_receiver, sender = ParticipantData) 

    
