# Generated by Django 5.0.3 on 2024-03-26 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estore', '0006_cartpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
