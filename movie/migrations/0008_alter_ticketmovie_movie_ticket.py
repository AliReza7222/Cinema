# Generated by Django 4.2.4 on 2023-08-21 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0007_alter_room_seat_reserved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketmovie',
            name='movie_ticket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='movie.movie'),
        ),
    ]