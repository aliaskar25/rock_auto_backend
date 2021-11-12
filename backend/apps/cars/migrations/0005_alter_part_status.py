# Generated by Django 3.2.8 on 2021-10-25 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_alter_part_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='status',
            field=models.CharField(choices=[('Out of stock', 'Oos'), ('In stock', 'Is')], default='In stock', max_length=16),
        ),
    ]
