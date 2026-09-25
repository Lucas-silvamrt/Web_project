from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Filme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=120)),
                ('ano', models.PositiveIntegerField()),
                ('sinopse', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
                ('nota', models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])),
                ('comentario', models.TextField(max_length=500)),
                ('criada_em', models.DateTimeField(auto_now_add=True)),
                ('filme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avaliacoes', to='filmes.filme')),
            ],
        ),
    ]
