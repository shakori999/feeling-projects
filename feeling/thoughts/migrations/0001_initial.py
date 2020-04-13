# Generated by Django 3.0.5 on 2020-04-13 01:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Thought',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recorded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('condition', models.IntegerField(choices=[(1, 'Joy'), (2, 'Passionate'), (3, 'Happy'), (4, 'Optimistic'), (5, 'Content'), (6, ' Bored'), (7, 'Pessimistic'), (8, 'Frustrated'), (9, 'Overwhelmed'), (10, 'Disappointed'), (11, 'Worried'), (12, 'Angry'), (13, 'Jealous'), (14, 'Insecure'), (15, 'Guilty'), (16, 'Fear'), (17, 'Grief'), (18, 'Despair')])),
                ('note', models.TextField(blank=True, default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thoughts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
