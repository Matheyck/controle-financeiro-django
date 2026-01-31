from django.db.models import Sum, Case, When, DecimalField, F
from core.models import Transacao

def calcular_saldo(queryset):
    return queryset.aggregate(
        saldo=Sum(
            Case(
                When(tipo='E', then='valor'),
                When(tipo='S', then=-1 * F('valor')),
                output_field=DecimalField()
            )
        )
    )['saldo'] or 0


def saldo_total():
    return calcular_saldo(Transacao.objects.all())


def saldo_mensal(ano, mes):
    qs = Transacao.objects.filter(
        data__year=ano,
        data__month=mes
    )
    return calcular_saldo(qs)


def saldo_por_categoria(ano=None, mes=None):
    qs = Transacao.objects.all()

    if ano and mes:
        qs = qs.filter(data__year=ano, data__month=mes)

    return qs.values(
        'categoria__nome'
    ).annotate(
        total=Sum(
            Case(
                When(tipo='E', then='valor'),
                When(tipo='S', then=-1 * F('valor')),
                output_field=DecimalField()
            )
        )
    )
