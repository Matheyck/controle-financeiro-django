from django.db import models
from .managers import TransacaoQuerySet

class Categoria(models.Model):
    TIPO_CHOICES = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )

    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)

    def __str__(self):
        return self.nome

class Transacao(models.Model):
    TIPO_CHOICES = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )
    
    objects = TransacaoQuerySet.as_manager()
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='transacoes'
    )

    def __str__(self):
        return f'{self.descricao} - {self.valor}'
