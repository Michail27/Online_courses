# Generated by Django 3.2.10 on 2021-12-16 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clases', '0004_alter_course_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_lecture', models.CharField(max_length=300)),
                ('presentation', models.FileField(upload_to='uploads/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='clases.course')),
                ('lecture_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]