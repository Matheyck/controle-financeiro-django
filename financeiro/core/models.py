from django.db import models
from .managers import TransacaoQuerySet
from django.core.exceptions import ValidationError  # ValidationError é uma classe que define uma exceção para o modelo
from django.utils import timezone  # timezone é um módulo que fornece funções para trabalhar com fusos horários

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
    
    def clean(self):  # clean é um método que valida o modelo
        # Regra 1: tipo da transação = tipo da categoria
        if self.categoria and self.tipo:  # if é uma condição que verifica se o tipo da transação é igual ao tipo da categoria
            if self.categoria.tipo != self.tipo:  # if é uma condição que verifica se o tipo da transação é igual ao tipo da categoria
                raise ValidationError(  # ValidationError é uma classe que define uma exceção para o modelo
                    'O tipo da transação deve ser igual ao tipo da categoria.'  # message é o mensagem da exceção
                )

        # Regra 2: bloquear data futura (se essa for a decisão)
        if self.data and self.data > timezone.now().date():  # timezone.now().date() é a data atual
            raise ValidationError(  # ValidationError é uma classe que define uma exceção para o modelo
                'Transações não podem ter data futura.'  # message é o mensagem da exceção
            )

    def save(self, *args, **kwargs):  # save é um método que salva o modelo no banco de dados
        self.full_clean()  # full_clean é um método que valida o modelo
        super().save(*args, **kwargs)  # super() é uma classe que chama o método save da classe pai
    
    class Meta:  # Meta é uma classe interna que define metadados para o modelo
        constraints = [  # constraints é uma lista de constraints para o modelo
            models.CheckConstraint(  # CheckConstraint é uma classe que define uma constraint para o modelo
                condition=models.Q(valor__gt=0),  # Q é uma classe que define uma query para o modelo
                name='valor_positivo'  # name é o nome da constraint
            ),
            models.CheckConstraint(  # CheckConstraint é uma classe que define uma constraint para o modelo
                condition=models.Q(tipo__in=['E', 'S']),  # Q é uma classe que define uma query para o modelo
                name='tipo_valido'  # name é o nome da constraint
            ),
        ]