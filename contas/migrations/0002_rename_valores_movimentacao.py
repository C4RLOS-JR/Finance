# Generated by Django 5.0.7 on 2024-08-09 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0001_initial'),
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Valores',
            new_name='Movimentacao',
        ),
    ]
