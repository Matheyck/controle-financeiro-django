from django.db import models
from django.db.models import Sum, Case, When, DecimalField, F

class TransacaoQuerySet(models.QuerySet):
    def saldo(self):
        return self.aggregate(
            saldo=Sum(
                Case(
                    When(tipo='E', then='valor'),
                    When(tipo='S', then=-1 * F('valor')),
                    output_field=DecimalField()
                )
            )
        )['saldo'] or 0

    def do_mes(self, ano, mes):
        return self.filter(data__year=ano, data__month=mes)