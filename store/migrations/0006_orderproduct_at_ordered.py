# Generated by Django 3.2.6 on 2022-07-05 20:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20220705_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='at_ordered',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
