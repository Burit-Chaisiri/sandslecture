# Generated by Django 3.0.4 on 2020-03-14 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0013_auto_20200314_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture_img',
            name='LectureKey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Lecture_img', to='Homepage.Lecture'),
        ),
    ]
