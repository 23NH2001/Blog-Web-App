# Generated by Django 4.1 on 2022-09-13 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_remove_user_model_fbprofile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='message',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
                ('email_address', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('date', models.DateField()),
            ],
        ),
    ]