# Generated by Django 4.2.10 on 2024-03-02 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('username', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('is_private', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Career',
                'verbose_name_plural': 'Careers',
            },
        ),
    ]