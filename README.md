# CineNotas 🎬

**Status:** protótipo local em desenvolvimento  
**Versão:** 0.2.0  
**Licença:** ainda não definida

**Instituição:** Centro Universitário de Brasília (CEUB)  
**Curso:** Ciência da Computação  
**Disciplina:** Desenvolvimento Web  
**Turma / semestre:** B 0726 / 4º semestre  
**Professor:** Felippe Pires Ferreira  
**Repositório:** [Lucas-silvamrt/Web_project](https://github.com/Lucas-silvamrt/Web_project)

> Este README descreve o código Django entregue neste pacote. O repositório GitHub deve receber estes arquivos atualizados para corresponder à documentação.

## Sumário

- [1. Descrição do projeto](#1-descrição-do-projeto)
- [2. Funcionalidades](#2-funcionalidades)
- [3. Demonstração](#3-demonstração)
- [4. Tecnologias utilizadas](#4-tecnologias-utilizadas)
- [5. Arquitetura](#5-arquitetura)
- [6. Organização dos diretórios](#6-organização-dos-diretórios)
- [7. Participantes](#7-participantes)
- [8. Como executar](#8-como-executar)
- [9. Configuração](#9-configuração)
- [10. Testes](#10-testes)
- [11. Uso de inteligência artificial](#11-uso-de-inteligência-artificial)
- [12. Contribuição e fluxo de trabalho](#12-contribuição-e-fluxo-de-trabalho)
- [13. Histórico de versões](#13-histórico-de-versões)
- [14. Limitações e próximos passos](#14-limitações-e-próximos-passos)
- [15. Licença, referências e contato](#15-licença-referências-e-contato)

## 1. Descrição do projeto

O CineNotas é um site simples para consultar filmes e compartilhar avaliações. Ele ajuda as pessoas a considerar outra opinião na hora de escolher o que assistir. A página inicial apresenta o catálogo; cada filme possui uma página com ano, sinopse, média das notas e comentários publicados.

O público-alvo são pessoas interessadas em filmes, principalmente filmes infantis. O administrador pode cadastrar, editar, excluir e importar filmes em telas próprias, depois de entrar com uma conta de equipe do Django. Visitantes podem avaliar sem criar uma conta.

### Objetivos do protótipo atual

- Exibir filmes cadastrados e seus detalhes.
- Receber comentários e notas de 1 a 5.
- Calcular e exibir a média das avaliações.
- Buscar por título e ano e apresentar um relatório imprimível.
- Oferecer consulta JSON e importar metadados de filmes de uma API externa.

O escopo final da atividade inclui outras funções descritas na especificação fornecida pelo professor. As decisões de análise e os documentos de especificação devem ser elaborados pelo aluno, conforme a regra acadêmica da disciplina.

## 2. Funcionalidades

| Funcionalidade | Descrição | Status |
| --- | --- | --- |
| Catálogo e detalhes | Exibe filmes, sinopses, notas médias e comentários. | Implementada |
| Avaliação | Recebe nome, nota de 1 a 5 e comentário. | Implementada |
| Gerenciamento próprio | Administrador cadastra, edita e exclui filmes em telas do site. | Implementada |
| Busca | Filtra filmes por parte do título e/ou ano. | Implementada |
| Relatório | Mostra quantidade de avaliações e média por filme; pode ser impresso ou salvo em PDF pelo navegador. | Implementada |
| API REST própria | Consulta pública de filmes em JSON, com filtros e resposta de erro. | Implementada (leitura) |
| API externa | Administrador importa título, ano e diretor de filmes do Studio Ghibli. | Implementada; depende do serviço externo |
| Publicação | Aplicação pública com HTTPS. | Pendente |

### Requisitos não funcionais observáveis

- **Persistência:** SQLite local; modelos e migrations do Django.
- **Validação:** formulários do Django validam os campos; nota de 1 a 5 e ano de 1888 a 2100.
- **Interface:** identidade CineNotas em tons de azul escuro, layout simples com grade adaptável e estilo próprio para impressão.
- **Acesso:** cadastro, edição, exclusão e importação exigem usuário com `is_staff=True`; visitantes consultam e avaliam.
- **Segurança:** formulários protegidos por CSRF; variáveis de ambiente disponíveis para configurações de produção, ainda não implantadas.

## 3. Demonstração

O projeto pode ser demonstrado localmente após seguir as instruções da seção 8. O arquivo `filmes_exemplo.json` contém três filmes para a demonstração: *Toy Story* (1995), *Procurando Nemo* (2003) e *Divertida Mente* (2015).

| Tela | Descrição | Caminho local |
| --- | --- | --- |
| Catálogo | Lista de filmes e médias. | `/` |
| Detalhes | Sinopse, comentários e formulário de avaliação. | `/filme/1/` |
| Gerenciamento | Cadastro, edição, exclusão e importação por equipe. | `/gerenciar/` |
| Relatório | Indicadores por filme, imprimíveis com Ctrl+P. | `/relatorio/` |
| API | Dados em JSON. | `/api/filmes/` |

Capturas de tela, vídeo e endereço de produção ainda não foram disponibilizados.

## 4. Tecnologias utilizadas

| Camada | Tecnologia | Informação do projeto |
| --- | --- | --- |
| Linguagem | Python | Executado com o Python instalado localmente. |
| Backend | Django | `requirements.txt` aceita versões `>=5.2,<6.0`. |
| Interface | Templates HTML e CSS | Arquivos próprios do projeto. |
| Banco de dados | SQLite | Configurado em `config/settings.py`. |
| Dados de exemplo | JSON | Carregado com `loaddata`. |
| API externa | Ghibli API | Consulta por HTTPS a um serviço comunitário. |
| Testes | Django TestCase | Quatro testes de fluxos principais. |

A API de leitura foi implementada com `JsonResponse` do Django. A integração externa usa a [Ghibli API comunitária](https://github.com/mazipan/ghibli-api), sem chave. Não há hospedagem configurada.

## 5. Arquitetura

O navegador solicita as páginas ao Django. As URLs encaminham a requisição às *views*, que consultam os *models* no SQLite e renderizam os templates HTML. O CSS é servido como arquivo estático durante o desenvolvimento local.

```text
Navegador → URLs e views Django → models → SQLite
                     ↓
              templates e CSS
```

As entidades atuais são `Filme` (título, ano e sinopse) e `Avaliacao` (filme, nome, nota, comentário e data). Um filme pode ter várias avaliações. A média é calculada a partir das notas registradas.

### Rotas atuais

| Método | Rota | Função |
| --- | --- | --- |
| `GET` | `/` | Catálogo e busca por `q` e `ano`. |
| `GET` | `/filme/<id>/` | Detalhes e avaliações. |
| `POST` | `/filme/<id>/` | Enviar avaliação válida. |
| `GET` | `/relatorio/` | Relatório imprimível. |
| `GET/POST` | `/gerenciar/` e subrotas | Manutenção e importação por administradores. |
| `GET` | `/api/filmes/` e `/api/filmes/<id>/` | API JSON somente leitura. |
| Vários | `/admin/` | Painel administrativo do Django. |

A [documentação da API](docs/API.md) detalha parâmetros, exemplos JSON e códigos HTTP. A integração externa é usada no fluxo de importação; uma indisponibilidade do serviço é informada ao administrador.

## 6. Organização dos diretórios

```text
.
├── README.md
└── CineNotas_Django/
    ├── .env.example
    ├── manage.py
    ├── requirements.txt
    ├── filmes_exemplo.json
    ├── docs/API.md
    ├── config/                 # configurações e URLs principais
    └── filmes/
        ├── admin.py
        ├── externo.py          # consulta à API externa
        ├── forms.py
        ├── models.py
        ├── tests.py
        ├── urls.py
        ├── views.py
        ├── migrations/
        ├── templates/filmes/
        └── static/filmes/style.css
```

A árvore representa a organização para o repositório GitHub; este ZIP contém somente a pasta da aplicação. Os documentos de análise, diagramas e evidências de segurança pedidos na especificação da disciplina ainda não estão incluídos.

## 7. Participantes

| Nome | Matrícula | Função no projeto |
| --- | --- | --- |
| Lucas Silva Martins | 22502092 | Responsável individual pelas etapas do projeto: planejamento, código, testes, documentação e apresentação. |

**Professor responsável:** Felippe Pires Ferreira.

## 8. Como executar

### Pré-requisitos

- Python instalado e disponível no terminal.
- Acesso à Internet para instalar as dependências na primeira execução.

Clone o repositório ou extraia o ZIP. Se usar o repositório GitHub, entre na pasta da aplicação:

```powershell
git clone https://github.com/Lucas-silvamrt/Web_project.git
cd Web_project\CineNotas_Django
```

Se usar o ZIP, abra no VS Code a pasta extraída que contém `manage.py`. A partir dessa pasta, no terminal do Windows:

```powershell
py -m venv .venv
```

Ative o ambiente. No **PowerShell**:

```powershell
.\.venv\Scripts\Activate.ps1
```

No **Prompt de Comando (CMD)**:

```bat
.venv\Scripts\activate.bat
```

Instale e execute:

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata filmes_exemplo.json
python manage.py runserver
```

Acesse **http://127.0.0.1:8000/**. O `loaddata` carrega ou atualiza os três filmes de exemplo com IDs 1, 2 e 3. Para interromper o servidor, pressione `Ctrl+C`.

Para administrar os filmes:

```powershell
python manage.py createsuperuser
python manage.py runserver
```

Acesse **http://127.0.0.1:8000/admin/** e entre com o usuário criado. Em Linux ou macOS, a ativação do ambiente virtual é `source .venv/bin/activate`.

**Implantação:** ainda não há URL pública informada. A documentação local da API está em `docs/API.md`.

**Prazos informados:** Fase 1 em **09/10/2026** e Fase 2 em **04/12/2026**.

## 9. Configuração

Para uso local, o site funciona sem definir variáveis de ambiente, com `DEBUG=True`, SQLite e chave exclusiva para demonstração. O arquivo `.env.example` mostra os nomes das variáveis usadas quando a configuração mudar. O Django não carrega `.env` automaticamente: configure essas variáveis no ambiente antes de executar o servidor de produção.

| Variável | Uso | Exemplo sem segredo |
| --- | --- | --- |
| `DJANGO_DEBUG` | `False` em produção. | `False` |
| `DJANGO_SECRET_KEY` | Chave própria, obrigatória se `DEBUG=False`. | valor privado |
| `DJANGO_ALLOWED_HOSTS` | Domínios aceitos, separados por vírgula. | `site.example` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Origens HTTPS permitidas para formulários. | `https://site.example` |

A publicação ainda exige hospedagem, HTTPS, serviço de arquivos estáticos e revisão do banco e das demais configurações. Não versionar `.env`, chaves ou bancos com dados sensíveis.

## 10. Testes

Execute na pasta que contém `manage.py`:

```powershell
python manage.py check
python manage.py test filmes
```

Os quatro testes automatizados verificam busca, relatório, respostas da API, controle de acesso e manutenção de filmes, importação sem duplicata e tratamento de falha do serviço externo. A resposta da API externa é simulada nos testes. A integração ao vivo depende da disponibilidade do serviço e do acesso à Internet. A cobertura percentual não foi medida. Os relatórios SAST e DAST exigidos na Fase 2 ainda estão pendentes.

## 11. Uso de inteligência artificial

**Houve uso de IA:** sim.  
**Ferramenta:** ChatGPT (OpenAI).

O ChatGPT auxiliou na criação da versão inicial do protótipo Django apresentada nesta conversa e na implementação das telas de gerenciamento, busca, relatório, API de leitura e integração externa. Também preparou e atualizou este README. Quando houve dificuldade com os filmes de exemplo, a ferramenta forneceu um arquivo `filmes_exemplo.json` atualizado com filmes reais para substituir os registros fictícios anteriores.

Lucas Silva Martins é o responsável individual por revisar o código, compreender seu funcionamento, tomar as decisões do projeto e apresentar o trabalho. A declaração acima registra a participação da ferramenta sem atribuir exclusivamente ao aluno partes produzidas com auxílio de IA.

A especificação da atividade informa que a **especificação do projeto deve ser elaborada individualmente pelo aluno, sem geração ou reescrita direta por IA**. Este README descreve o estado observável do protótipo e não substitui o documento de visão, os requisitos, diagramas ou as justificativas de projeto que devem refletir as decisões do estudante. A imagem da política de IA citada no modelo do README não foi fornecida neste pacote.

## 12. Contribuição e fluxo de trabalho

O trabalho é individual. O histórico de alterações deve ser mantido no [repositório do projeto](https://github.com/Lucas-silvamrt/Web_project), com commits distribuídos ao longo do desenvolvimento e documentação correspondente às entregas. Não há fluxo de revisão em grupo a registrar.

A origem a partir do template oficial e a publicação dos documentos exigidos devem ser conferidas pelo aluno antes da entrega.

## 13. Histórico de versões

| Versão | Data | Descrição |
| --- | --- | --- |
| `0.2.0` | 25/09/2026 | Gerenciamento próprio, busca, relatório, API JSON, importação externa, testes e documentação da API. |
| `0.1.0` | 25/09/2026 | Protótipo local com catálogo, detalhes, avaliações, painel administrativo e filmes de exemplo. |

Essas versões descrevem entregas locais; não são tags publicadas no GitHub. Consulte o repositório para o histórico de commits.

## 14. Limitações e próximos passos

Ainda faltam hospedagem pública com HTTPS, documentação de análise e diagramas de autoria do aluno, evidências de teste ampliadas, relatório SAST/DAST e apresentação final. A importação externa depende de um serviço comunitário que pode ficar indisponível. A API própria é somente leitura e devolve até 100 filmes, sem paginação. A configuração atual usa SQLite e ainda não foi validada para produção.

Os prazos informados são **09/10/2026 (Fase 1)** e **04/12/2026 (Fase 2)**. As decisões e justificativas técnicas da especificação devem ser registradas pelo aluno conforme as regras da disciplina.

## 15. Licença, referências e contato

**Licença/condições de uso:** ainda não definidas pelo autor. A disponibilização do código em um repositório, por si só, não define uma licença de reutilização.  
**Contato:** [repositório GitHub do projeto](https://github.com/Lucas-silvamrt/Web_project); nenhum endereço de e-mail foi informado.  
**Referência acadêmica:** *Especificação do Trabalho Django*, disciplina Desenvolvimento Web, professor Felippe Pires Ferreira (documento fornecido para a atividade).  
**Documentação técnica:** [Django](https://docs.djangoproject.com/).

Documentação da API: [`docs/API.md`](docs/API.md). Links para diagramas, apresentação, aplicação publicada e evidências de segurança serão adicionados quando esses artefatos existirem. Fonte externa: [Ghibli API](https://github.com/mazipan/ghibli-api).
