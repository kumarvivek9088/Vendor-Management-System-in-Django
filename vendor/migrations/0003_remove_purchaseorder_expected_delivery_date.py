# Generated by Django 5.0.4 on 2024-05-02 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_purchaseorder_expected_delivery_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorder',
            name='expected_delivery_date',
        ),
    ]
