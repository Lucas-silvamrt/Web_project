from unittest.mock import patch
from io import BytesIO
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .externo import ServicoIndisponivel, listar_filmes_externos
from .models import Avaliacao, Filme


class FluxosDoSite(TestCase):
    def setUp(self):
        self.filme = Filme.objects.create(titulo='Toy Story', ano=1995, sinopse='Brinquedos de Andy.')
        self.admin = get_user_model().objects.create_user('lucas', password='senha-de-teste', is_staff=True)

    def test_busca_relatorio_e_api(self):
        Avaliacao.objects.create(filme=self.filme, nome='Ana', nota=4, comentario='Bom filme')
        self.assertContains(self.client.get('/?q=Toy&ano=1995'), 'Toy Story')
        self.assertNotContains(self.client.get('/?q=Inexistente'), 'Toy Story')
        self.assertContains(self.client.get('/relatorio/'), '4,0/5')
        dados = self.client.get('/api/filmes/?ano=1995').json()['resultados']
        self.assertEqual(dados[0]['nota_media'], 4.0)
        self.assertEqual(self.client.get('/api/filmes/?ano=abc').status_code, 400)
        self.assertEqual(self.client.get('/api/filmes/999/').status_code, 404)

    def test_crud_protegido(self):
        self.assertEqual(self.client.get('/gerenciar/').status_code, 302)
        self.assertEqual(self.client.post('/gerenciar/novo/', {'titulo':'Outro','ano':2020,'sinopse':'Teste'}).status_code, 302)
        self.assertEqual(Filme.objects.count(), 1)
        self.client.force_login(self.admin)
        self.assertEqual(self.client.post('/gerenciar/novo/', {'titulo':'Outro','ano':2020,'sinopse':'Teste'}).status_code, 302)
        outro = Filme.objects.get(titulo='Outro')
        self.client.post(reverse('editar_filme', args=[outro.pk]), {'titulo':'Novo título','ano':2020,'sinopse':'Teste'})
        self.assertTrue(Filme.objects.filter(titulo='Novo título').exists())
        self.client.post(reverse('excluir_filme', args=[outro.pk]))
        self.assertFalse(Filme.objects.filter(pk=outro.pk).exists())

    @patch('filmes.views.listar_filmes_externos')
    def test_importacao_e_falha_da_api_externa(self, consulta):
        self.client.force_login(self.admin)
        consulta.return_value = [{'titulo':'Meu Amigo Totoro','ano':1988,'sinopse':'Duas irmãs e um amigo da floresta.'}]
        self.assertEqual(self.client.get('/gerenciar/importar/').status_code, 200)
        self.client.post('/gerenciar/importar/', {'indice':'0'})
        self.assertTrue(Filme.objects.filter(titulo='Meu Amigo Totoro').exists())
        self.client.post('/gerenciar/importar/', {'indice':'0'})
        self.assertEqual(Filme.objects.filter(titulo='Meu Amigo Totoro').count(), 1)
        consulta.side_effect = ServicoIndisponivel('Serviço indisponível')
        self.assertContains(self.client.get('/gerenciar/importar/'), 'Serviço indisponível')

    @patch('filmes.externo.urlopen')
    def test_formato_da_api_externa(self, urlopen):
        class Resposta(BytesIO):
            status = 200
        urlopen.return_value.__enter__.return_value = Resposta(b'{"data":[{"title":"My Neighbor Totoro","release_date":"1988","director":"Hayao Miyazaki"}]}')
        filmes = listar_filmes_externos()
        self.assertEqual(filmes[0]['ano'], 1988)
        self.assertIn('Direção: Hayao Miyazaki', filmes[0]['sinopse'])
