# Generated by Django 3.1.6 on 2021-03-28 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_data', '0011_auto_20210328_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='image',
            field=models.ImageField(upload_to='certificates/'),
        ),
    ]