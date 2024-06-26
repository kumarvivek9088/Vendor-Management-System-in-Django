# Generated by Django 5.0.4 on 2024-05-02 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='expected_delivery_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Expected delivery date of the order'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateTimeField(verbose_name='Actual delivery date of the order'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.vendors', verbose_name='Link to the vendor model'),
        ),
        migrations.AlterField(
            model_name='vendors',
            name='average_response_time',
            field=models.FloatField(default=0, verbose_name='Average time taken to acknowledge purchase orders'),
        ),
        migrations.AlterField(
            model_name='vendors',
            name='fulfillment_rate',
            field=models.FloatField(default=0, verbose_name='Percentage of purchase orders fulfilled successfully'),
        ),
        migrations.AlterField(
            model_name='vendors',
            name='on_time_delivery_rate',
            field=models.FloatField(default=0, verbose_name=' Tracks the percentage of on-time deliveries'),
        ),
        migrations.AlterField(
            model_name='vendors',
            name='quality_rating_avg',
            field=models.FloatField(default=0, verbose_name='Average rating of quality based on purchase orders'),
        ),
        migrations.AlterField(
            model_name='vendors',
            name='vendor_code',
            field=models.CharField(max_length=500, unique=True, verbose_name='A unique identifier for the vendor'),
        ),
    ]
