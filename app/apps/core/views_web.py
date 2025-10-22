# -*- coding: utf-8 -*-
"""
Views Web do app Core
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from datetime import datetime, timedelta

from apps.contas_pagar.models import ContaPagar
from apps.contas_receber.models import ContaReceber
from apps.parcelas.models import Parcela


def dashboard(request):
    """
    View do dashboard principal
    """
    context = {
        'page_title': 'Dashboard',
        'user': request.user,
    }
    return render(request, 'dashboard/dashboard.html', context)


def dashboard_stats(request):
    """
    API para estatísticas do dashboard
    """
    try:
        # Estatísticas de contas a receber
        contas_receber = ContaReceber.objects.filter(ativo=True)
        total_receber = contas_receber.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        valor_recebido = sum(conta.get_valor_recebido() for conta in contas_receber)
        valor_pendente_receber = total_receber - valor_recebido
        
        # Estatísticas de contas a pagar
        contas_pagar = ContaPagar.objects.filter(ativo=True)
        total_pagar = contas_pagar.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        valor_pago = sum(conta.get_valor_pago() for conta in contas_pagar)
        valor_pendente_pagar = total_pagar - valor_pago
        
        # Saldo líquido
        saldo_liquido = valor_pendente_receber - valor_pendente_pagar
        
        # Parcelas vencidas
        parcelas_vencidas = Parcela.objects.filter(
            ativo=True,
            status='VENCIDA'
        ).count()
        
        # Contas recentes
        contas_receber_recentes = contas_receber.order_by('-criado_em')[:5]
        contas_pagar_recentes = contas_pagar.order_by('-criado_em')[:5]
        
        # Parcelas vencidas recentes
        parcelas_vencidas_recentes = Parcela.objects.filter(
            ativo=True,
            status='VENCIDA'
        ).order_by('data_vencimento')[:10]
        
        data = {
            'total_receber': float(total_receber),
            'valor_recebido': float(valor_recebido),
            'valor_pendente_receber': float(valor_pendente_receber),
            'total_pagar': float(total_pagar),
            'valor_pago': float(valor_pago),
            'valor_pendente_pagar': float(valor_pendente_pagar),
            'saldo_liquido': float(saldo_liquido),
            'parcelas_vencidas': parcelas_vencidas,
            'contas_receber_recentes': [
                {
                    'id': conta.id,
                    'cliente_nome': conta.cliente.nome,
                    'valor_total': float(conta.valor_total),
                    'data_emissao': conta.data_emissao.isoformat(),
                    'status': conta.status,
                    'status_display': conta.get_status_display()
                }
                for conta in contas_receber_recentes
            ],
            'contas_pagar_recentes': [
                {
                    'id': conta.id,
                    'fornecedor_nome': conta.fornecedor.razao_social,
                    'valor_total': float(conta.valor_total),
                    'data_emissao': conta.data_emissao.isoformat(),
                    'status': conta.status,
                    'status_display': conta.get_status_display()
                }
                for conta in contas_pagar_recentes
            ],
            'parcelas_vencidas_recentes': [
                {
                    'id': parcela.id,
                    'numero_parcela': parcela.numero_parcela,
                    'valor': float(parcela.valor),
                    'data_vencimento': parcela.data_vencimento.isoformat(),
                    'dias_atraso': (datetime.now().date() - parcela.data_vencimento).days
                }
                for parcela in parcelas_vencidas_recentes
            ]
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def fluxo_caixa_data(request):
    """
    API para dados do fluxo de caixa
    """
    try:
        # Últimos 12 meses
        meses = []
        receitas = []
        despesas = []
        
        for i in range(12):
            data = datetime.now().date() - timedelta(days=30 * i)
            mes_inicio = data.replace(day=1)
            mes_fim = (mes_inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            # Receitas do mês
            receita_mes = ContaReceber.objects.filter(
                ativo=True,
                data_emissao__range=[mes_inicio, mes_fim]
            ).aggregate(Sum('valor_total'))['valor_total__sum'] or 0
            
            # Despesas do mês
            despesa_mes = ContaPagar.objects.filter(
                ativo=True,
                data_emissao__range=[mes_inicio, mes_fim]
            ).aggregate(Sum('valor_total'))['valor_total__sum'] or 0
            
            meses.insert(0, mes_inicio.strftime('%b'))
            receitas.insert(0, float(receita_mes))
            despesas.insert(0, float(despesa_mes))
        
        data = {
            'meses': meses,
            'receitas': receitas,
            'despesas': despesas
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def despesas_por_categoria_data(request):
    """
    API para dados de despesas por categoria
    """
    try:
        from apps.tipos_despesa.models import TipoDespesa
        
        categorias = []
        valores = []
        cores = []
        
        for categoria, _ in TipoDespesa.CategoriaDespesa.choices:
            # Contar despesas por categoria
            contas_categoria = ContaPagar.objects.filter(
                ativo=True,
                tipos_despesa__categoria=categoria
            ).aggregate(Sum('valor_total'))['valor_total__sum'] or 0
            
            if contas_categoria > 0:
                categorias.append(categoria.replace('_', ' ').title())
                valores.append(float(contas_categoria))
                cores.append('#198754')  # Cor padrão
        
        data = {
            'categorias': categorias,
            'valores': valores,
            'cores': cores
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

