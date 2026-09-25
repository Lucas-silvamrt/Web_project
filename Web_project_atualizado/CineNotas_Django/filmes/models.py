from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Filme(models.Model):
    titulo = models.CharField(max_length=120)
    ano = models.PositiveIntegerField(validators=[MinValueValidator(1888), MaxValueValidator(2100)])
    sinopse = models.TextField()

    def __str__(self):
        return self.titulo


class Avaliacao(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='avaliacoes')
    nome = models.CharField(max_length=60)
    nota = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(max_length=500)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} — {self.filme.titulo} ({self.nota}/5)'
