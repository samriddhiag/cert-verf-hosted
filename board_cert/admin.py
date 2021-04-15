from django.contrib import admin
from .models import Board_Certificate, Board_member_details
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
# Register your models here.

class BoardResource(resources.ModelResource):
    class Meta:
        model = Board_member_details
        fields = ('id', 'Board_Full_Name', 'Designation', 'Photo', "Description_n_about")

class BoardDataAdmin(ImportExportActionModelAdmin):
    resource_class = BoardResource
    exclude = ["slug"]
    list_display = ('id', 'Board_Full_Name', 'Designation', 'Photo', "Description_n_about", "slug")

admin.site.register(Board_member_details, BoardDataAdmin)
admin.site.register(Board_Certificate)


