# Generated by Django 3.2.6 on 2022-07-13 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
