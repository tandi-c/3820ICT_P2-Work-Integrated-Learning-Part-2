# Generated by Django 3.2 on 2021-09-14 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0013_auto_20210914_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
