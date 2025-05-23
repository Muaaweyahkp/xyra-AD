# Generated by Django 5.2 on 2025-04-10 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('subject', models.CharField(max_length=120)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='testimonials')),
                ('position', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
    ]
