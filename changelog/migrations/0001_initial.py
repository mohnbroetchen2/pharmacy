# Generated by Django 2.1.7 on 2019-03-12 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_type', models.CharField(choices=[('new', 'new'), ('adaption', 'adaption'), ('bugfix', 'bugfix'), ('deletion', 'deletion')], default='adaption', max_length=100)),
                ('version', models.CharField(max_length=200)),
                ('entry_date', models.DateField(auto_now_add=True)),
                ('short_text', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]
