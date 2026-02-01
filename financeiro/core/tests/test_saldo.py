import pytest  # pytest é uma biblioteca para testes unitários
from decimal import Decimal  # Decimal é uma classe que representa um número decimal
from datetime import date  # date é uma classe que representa uma data
from core.models import Categoria, Transacao  # Categoria e Transacao são classes que representam uma categoria e uma transação
from core.services.financeiro_service import saldo_total  # saldo_total é uma função que calcula o saldo total

@pytest.mark.django_db  # pytest.mark.django_db é um decorador que indica que o teste é um teste de Django
def test_saldo_total_calculo_correto():  # test_saldo_total_calculo_correto é uma função que testa se o saldo total é calculado corretamente
    salario = Categoria.objects.create(nome='Salário', tipo='E')  # Cria uma categoria de entrada
    aluguel = Categoria.objects.create(nome='Aluguel', tipo='S')  # Cria uma categoria de saída

    Transacao.objects.create(  # Cria uma transação de entrada
        descricao='Salário',  # Descrição da transação
        valor=Decimal('3000.00'),  # Valor da transação
        data=date.today(),  # Data da transação
        tipo='E',  # Tipo da transação
        categoria=salario  # Categoria da transação
    )

    Transacao.objects.create(  # Cria uma transação de saída
        descricao='Aluguel',  # Descrição da transação
        valor=Decimal('1000.00'),  # Valor da transação
        data=date.today(),  # Data da transação
        tipo='S',  # Tipo da transação
        categoria=aluguel  # Categoria da transação
    )

    assert saldo_total() == Decimal('2000.00')  # Verifica se o saldo total é igual a 2000.00
