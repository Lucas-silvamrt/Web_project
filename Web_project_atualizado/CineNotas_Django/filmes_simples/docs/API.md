# API REST do CineNotas (versão 1)

A API é pública, somente leitura e retorna JSON. URL-base local: `http://127.0.0.1:8000`. Não há autenticação, paginação nem chave de acesso. No máximo 100 filmes são retornados na listagem. As avaliações individuais não são expostas.

## GET /api/filmes/

Lista filmes em ordem alfabética. Parâmetros opcionais: `q` (trecho do título, até 120 caracteres) e `ano` (número de 1888 a 2100).

Exemplo: `GET /api/filmes/?q=Toy&ano=1995`

Resposta `200 OK`:

```json
{"resultados":[{"id":1,"titulo":"Toy Story","ano":1995,"sinopse":"...","nota_media":4.5,"total_avaliacoes":2}]}
```

Ano inválido: `400 Bad Request`, com `{"erro":"O ano deve ser um número entre 1888 e 2100."}`.

## GET /api/filmes/<id>/

Retorna um filme com os mesmos campos da listagem. Um ID inexistente retorna `404 Not Found` com `{"erro":"Filme não encontrado."}`. Outros métodos retornam `405 Method Not Allowed` em ambas as rotas.

## API externa usada pelo projeto

A página protegida `/gerenciar/importar/` consulta `GET https://ghibli-api.vercel.app/api/films` para listar filmes do Studio Ghibli e permitir que o administrador adicione um deles ao catálogo local. São usados título, ano de lançamento e descrição. A requisição tem timeout de cinco segundos; indisponibilidade e formato inválido são informados na interface. A API é comunitária e pode ficar indisponível. Consulte o [projeto da API](https://github.com/mazipan/ghibli-api) para informações da fonte.
