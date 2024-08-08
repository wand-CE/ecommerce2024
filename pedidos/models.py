from django.db import models

from catproduto.models import Produto


class Pedido(models.Model):
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=70)
    email = models.EmailField()
    endereco = models.CharField(max_length=200)
    cep = models.CharField(max_length=10)
    cidade = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)
    pago = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ('-criado',)

    def __str__(self):
        return f'Pedido do {self.nome}  {self.sobrenome}'

    def get_total(self):
        return sum(item.get_custo() for item in self.itens_pedido.all())


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens_pedido',
                               on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, related_name='itens_produto',
                                on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Item Pedido'
        verbose_name_plural = 'Itens Pedido'

    def __str__(self):
        return self.id

    def get_custo(self):
        return self.preco * self.quantidade