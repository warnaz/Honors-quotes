# Generated by Django 4.1.1 on 2023-01-18 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_comment_liked_commentlike'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoteshonors',
            name='design',
            field=models.CharField(choices=[('D1', 'Design one'), ('D2', 'Design two'), ('D3', 'Design three')], default='D1', max_length=2),
        ),
    ]
