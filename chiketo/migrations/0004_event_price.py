# Generated by Django 5.1 on 2024-10-11 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chiketo', '0003_alter_booking_pay'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]