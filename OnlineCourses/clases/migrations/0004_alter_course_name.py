# Generated by Django 3.2.10 on 2021-12-16 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clases', '0003_alter_course_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
