# Generated by Django 5.0.6 on 2024-08-03 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comapp', '0006_remove_payment_razorpay_order_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='opay_transaction_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
