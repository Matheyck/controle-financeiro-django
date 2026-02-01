import pytest
from django.db import IntegrityError
from datetime import date
from core.models import Categoria, Transacao
from decimal import Decimal
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_nao_permite_valor_negativo():
    categoria = Categoria.objects.create(nome='Aluguel', tipo='S')

    with pytest.raises(IntegrityError):
        Transacao.objects.create(
            descricao='Teste inválido',
            valor=Decimal('-100.00'),
            data=date.today(),
            tipo='S',
            categoria=categoria
        )

@pytest.mark.django_db
def test_nao_permite_tipo_invalido():
    categoria = Categoria.objects.create(nome='Alimentação', tipo='S')

    with pytest.raises(IntegrityError):
        Transacao.objects.create(
            descricao='Tipo inválido',
            valor=Decimal('100.00'),
            data=date.today(),
            tipo='X',
            categoria=categoria
        )

@pytest.mark.django_db
def test_tipo_transacao_deve_bater_com_categoria():
    categoria = Categoria.objects.create(nome='Salário', tipo='E')

    transacao = Transacao(
        descricao='Erro lógico',
        valor=Decimal('1000.00'),
        data=date.today(),
        tipo='S',
        categoria=categoria
    )

    with pytest.raises(ValidationError):
        transacao.full_clean()