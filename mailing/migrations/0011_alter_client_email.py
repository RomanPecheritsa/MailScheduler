# Generated by Django 5.1.1 on 2024-10-24 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0010_alter_mailing_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="email",
            field=models.EmailField(max_length=254, verbose_name="почта"),
        ),
    ]
