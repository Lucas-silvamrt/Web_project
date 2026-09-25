from django import forms
from .models import Avaliacao, Filme


class FilmeForm(forms.ModelForm):
    class Meta:
        model = Filme
        fields = ['titulo', 'ano', 'sinopse']
        widgets = {'sinopse': forms.Textarea(attrs={'rows': 5})}


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nome', 'nota', 'comentario']
        widgets = {
            'nota': forms.Select(choices=[(n, f'{n} estrela(s)') for n in range(1, 6)]),
            'comentario': forms.Textarea(attrs={'rows': 4}),
        }
