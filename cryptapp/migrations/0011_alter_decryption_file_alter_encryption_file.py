# Generated by Django 4.0.5 on 2022-09-17 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptapp', '0010_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decryption',
            name='file',
            field=models.FileField(upload_to='decryted'),
        ),
        migrations.AlterField(
            model_name='encryption',
            name='file',
            field=models.FileField(upload_to='encrypted'),
        ),
    ]
