# Generated by Django 4.1.5 on 2023-01-28 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0002_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='image/gosling.jpg', upload_to='media/'),
        ),
    ]
