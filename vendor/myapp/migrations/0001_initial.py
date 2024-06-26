# Generated by Django 5.0.4 on 2024-05-03 19:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VendorModel',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('contact_details', models.TextField()),
                ('address', models.TextField()),
                ('vendor_code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('on_time_delivery_rate', models.FloatField()),
                ('quality_rating_avg', models.FloatField()),
                ('average_response_time', models.FloatField()),
                ('fulfilment_rate', models.FloatField()),
            ],
        ),
    ]
