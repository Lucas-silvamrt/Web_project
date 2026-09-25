"""Consulta pública ao catálogo de filmes da API comunitária do Studio Ghibli."""
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

URL_FILMES = 'https://ghibli-api.vercel.app/api/films'


class ServicoIndisponivel(Exception):
    pass


def listar_filmes_externos():
    try:
        pedido = Request(URL_FILMES, headers={'User-Agent': 'CineNotas/0.2 (projeto academico)', 'Accept': 'application/json'})
        with urlopen(pedido, timeout=5) as resposta:
            if resposta.status != 200:
                raise ServicoIndisponivel('A consulta externa não está disponível agora.')
            dados = json.load(resposta)
        if not isinstance(dados, dict) or not isinstance(dados.get('data'), list):
            raise ValueError('Formato inesperado')
        filmes = []
        for item in dados['data'][:100]:
            if not isinstance(item, dict):
                continue
            titulo = str(item.get('title') or '').strip()[:120]
            ano_texto = str(item.get('release_date') or '')
            diretor = str(item.get('director') or '').strip()[:120]
            sinopse = f'Filme do Studio Ghibli. Direção: {diretor}.' if diretor else 'Filme do Studio Ghibli.'
            if titulo and ano_texto.isdigit() and 1888 <= int(ano_texto) <= 2100:
                filmes.append({'titulo': titulo, 'ano': int(ano_texto), 'sinopse': sinopse})
        return filmes
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as erro:
        raise ServicoIndisponivel('A consulta externa não está disponível agora. Tente novamente mais tarde.') from erro
