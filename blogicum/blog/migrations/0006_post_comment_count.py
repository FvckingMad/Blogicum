# Generated by Django 3.2.16 on 2023-09-24 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comment_count',
            field=models.IntegerField(default=0, verbose_name='Кол-во комментариев'),
        ),
    ]
