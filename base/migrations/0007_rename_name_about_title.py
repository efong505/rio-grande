# Generated by Django 4.0.5 on 2022-07-10 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_post_updated_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='about',
            old_name='name',
            new_name='title',
        ),
    ]
