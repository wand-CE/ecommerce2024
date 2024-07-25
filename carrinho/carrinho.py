from decimal import Decimal

from django.conf import settings
from django.contrib.sites import requests
from django.http import request

from catproduto.models import Produto


class Carrinho:
    def __init__(self):
        """
        Inicializa o carrinho de compras
        """
        self.session = request.session
        carrinho = self.session.get(settings.CART_SESSION_ID)
        if not carrinho:
            # salva um carrinho vazio na sessão
            carrinho = self.session[settings.CART_SESSION_ID] = {}
        self.carrinho = carrinho

    def addProduto(self, produto, quantidade=1, alterar_quant=False):
        """
        Adiciona um produto ao carrinho ou atualiza a quantidade de um determinado
        produto
        :param produto: produto a ser adicionado ou alterado a quant
        :param quantidade: A quantidade de unidades do produto a ser adicionado
        :param alterar_quant: Quando necessário alterar a quantidade do produto no carrinho
        :return :
        """
        id_produto = str(produto.id)
        if id_produto not in self.carrinho:
            self.carrinho[id_produto] = {'quantidade': quantidade, 'preco': str(produto.preco)}
        if alterar_quant:
            self.carrinho[id_produto]['quantidade'] = quantidade
        else:
            self.carrinho[id_produto]['quantidade'] += quantidade
        self._salvar()

    def _salvar(self):
        self.session.modified = True

    def remover_produto(self, produto):
        """
        Remove um produto do carrinho
        :param  produto: o produto a ser removido
        :return:
        """
        id_produto = str(produto.id)
        if id_produto not in self.carrinho:
            del self.carrinho[id_produto]
            self._salvar()

    def __iter__(self):
        """
        Itera sobre o carrinho e obtem os produtos do banco de dados
        :return
        """
        ids_produtos = self.carrinho.keys()
        produtos = Produto.objects.filter(id__in=ids_produtos)
        carrinho = self.carrinho.copy()
        for p in produtos:
            carrinho[str(p.id)]['produto'] = p

        for item in carrinho.values():
            item['preco'] = Decimal(item['preco'])
            item['total'] = item['preco'] * item['quantidade']

            yield item

    def __len__(self):
        """
        Soma as quantidades de itens que o carrinho possui
        : return: A quantidade de itens do carrinho
        """
        return sum(item['quantidade'] for item in self.carrinho.values())

    def get_preco_total(self):
        return sum(Decimal(item['preco']) * item['quantidade'] for item in self.carrinho.values())

    def limpar(self):
        """

        """
        del self.session[settings.CART_SESSION_ID]
        self._salvar()
