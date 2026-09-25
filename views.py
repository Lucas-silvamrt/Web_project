from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .externo import ServicoIndisponivel, listar_filmes_externos
from .forms import AvaliacaoForm, FilmeForm
from .models import Filme


def filmes_com_notas():
    return Filme.objects.annotate(media=Avg('avaliacoes__nota'), total=Count('avaliacoes'))


def filtros(request, queryset):
    q = request.GET.get('q', '').strip()[:120]
    ano = request.GET.get('ano', '').strip()
    if q:
        queryset = queryset.filter(titulo__icontains=q)
    if ano:
        if not ano.isdigit() or not 1888 <= int(ano) <= 2100:
            return None, q, ano
        queryset = queryset.filter(ano=int(ano))
    return queryset, q, ano


def catalogo(request):
    filmes, q, ano = filtros(request, filmes_com_notas())
    if filmes is None:
        filmes = Filme.objects.none()
    return render(request, 'filmes/catalogo.html', {'filmes': filmes.order_by('titulo'), 'q': q, 'ano': ano})


def detalhe(request, pk):
    filme = get_object_or_404(Filme, pk=pk)
    enviado = False
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.filme = filme
            avaliacao.save()
            return redirect(reverse('detalhe', args=[filme.pk]) + '?enviado=1')
    else:
        form = AvaliacaoForm()
        enviado = request.GET.get('enviado') == '1'
    avaliacoes = filme.avaliacoes.order_by('-criada_em')
    media = avaliacoes.aggregate(valor=Avg('nota'))['valor']
    return render(request, 'filmes/detalhe.html', {
        'filme': filme, 'form': form, 'avaliacoes': avaliacoes, 'media': media, 'enviado': enviado,
    })


def relatorio(request):
    filmes = filmes_com_notas().order_by('titulo')
    totais = Filme.objects.aggregate(filmes=Count('id'))
    from .models import Avaliacao
    avaliacoes = Avaliacao.objects.count()
    return render(request, 'filmes/relatorio.html', {'filmes': filmes, 'total_filmes': totais['filmes'], 'total_avaliacoes': avaliacoes})


def serializar_filme(filme):
    return {'id': filme.pk, 'titulo': filme.titulo, 'ano': filme.ano, 'sinopse': filme.sinopse,
            'nota_media': round(filme.media, 2) if filme.media is not None else None,
            'total_avaliacoes': filme.total}


def api_filmes(request):
    if request.method != 'GET':
        return JsonResponse({'erro': 'Método não permitido.'}, status=405)
    filmes, q, ano = filtros(request, filmes_com_notas())
    if filmes is None:
        return JsonResponse({'erro': 'O ano deve ser um número entre 1888 e 2100.'}, status=400)
    return JsonResponse({'resultados': [serializar_filme(f) for f in filmes.order_by('titulo')[:100]]})


def api_filme(request, pk):
    if request.method != 'GET':
        return JsonResponse({'erro': 'Método não permitido.'}, status=405)
    filme = filmes_com_notas().filter(pk=pk).first()
    if filme is None:
        return JsonResponse({'erro': 'Filme não encontrado.'}, status=404)
    return JsonResponse(serializar_filme(filme))


@staff_member_required
def gerenciar(request):
    return render(request, 'filmes/gerenciar.html', {'filmes': Filme.objects.order_by('titulo')})


@staff_member_required
@require_http_methods(['GET', 'POST'])
def novo_filme(request):
    form = FilmeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Filme cadastrado com sucesso.')
        return redirect('gerenciar')
    return render(request, 'filmes/filme_form.html', {'form': form, 'titulo': 'Novo filme'})


@staff_member_required
@require_http_methods(['GET', 'POST'])
def editar_filme(request, pk):
    filme = get_object_or_404(Filme, pk=pk)
    form = FilmeForm(request.POST or None, instance=filme)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Filme atualizado com sucesso.')
        return redirect('gerenciar')
    return render(request, 'filmes/filme_form.html', {'form': form, 'titulo': 'Editar filme'})


@staff_member_required
@require_http_methods(['GET', 'POST'])
def excluir_filme(request, pk):
    filme = get_object_or_404(Filme, pk=pk)
    if request.method == 'POST':
        filme.delete()
        messages.success(request, 'Filme excluído com sucesso.')
        return redirect('gerenciar')
    return render(request, 'filmes/excluir_filme.html', {'filme': filme})


@staff_member_required
@require_http_methods(['GET', 'POST'])
def importar_filme(request):
    try:
        externos = listar_filmes_externos()
    except ServicoIndisponivel as erro:
        return render(request, 'filmes/importar.html', {'erro': str(erro), 'filmes': []})
    if request.method == 'POST':
        try:
            indice = int(request.POST.get('indice', '-1'))
            escolhido = externos[indice] if indice >= 0 else None
        except (ValueError, IndexError):
            escolhido = None
        if escolhido is None:
            messages.error(request, 'Escolha um filme válido da lista.')
        elif Filme.objects.filter(titulo__iexact=escolhido['titulo'], ano=escolhido['ano']).exists():
            messages.warning(request, 'Este filme já está no catálogo.')
        else:
            Filme.objects.create(**escolhido)
            messages.success(request, 'Filme importado para o catálogo.')
            return redirect('gerenciar')
    return render(request, 'filmes/importar.html', {'filmes': list(enumerate(externos))})
