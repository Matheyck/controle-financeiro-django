from django.shortcuts import render
from datetime import date
from core.services.financeiro_service import (
    saldo_total,
    saldo_mensal,
    saldo_por_categoria
)

def dashboard(request):
    hoje = date.today()

    context = {
        'saldo_total': saldo_total(),
        'saldo_mes': saldo_mensal(hoje.year, hoje.month),
        'por_categoria': saldo_por_categoria(hoje.year, hoje.month),
    }

    return render(request, 'core/dashboard.html', context)
