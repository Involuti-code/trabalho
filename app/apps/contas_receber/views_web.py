# -*- coding: utf-8 -*-
"""
Views Web do app Contas a Receber
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
import json

from .models import ContaReceber
from .serializers import ContaReceberSerializer
from apps.clientes.models import Cliente
from apps.tipos_receita.models import TipoReceita


def contas_receber_list(request):
    """View para listagem de contas a receber"""
    clientes = Cliente.objects.filter(ativo=True)
    tipos_receita = TipoReceita.objects.filter(ativo=True)
    return render(request, 'contas_receber/list.html', {
        'page_title': 'Contas a Receber',
        'clientes': clientes,
        'tipos_receita': tipos_receita,
    })


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def contas_receber_api(request, conta_id=None):
    """API para CRUD de contas a receber"""
    try:
        if request.method == 'GET':
            if conta_id:
                try:
                    conta = ContaReceber.objects.get(id=conta_id)
                    serializer = ContaReceberSerializer(conta)
                    return JsonResponse(serializer.data)
                except ContaReceber.DoesNotExist:
                    return JsonResponse({'error': 'Conta não encontrada'}, status=404)
            else:
                contas = ContaReceber.objects.all()
                
                ativo = request.GET.get('ativo')
                if ativo is not None:
                    contas = contas.filter(ativo=ativo.lower() == 'true')
                
                search = request.GET.get('search')
                if search:
                    contas = contas.filter(
                        Q(numero_documento__icontains=search) | 
                        Q(descricao__icontains=search) |
                        Q(cliente__nome__icontains=search)
                    )
                
                ordering = request.GET.get('ordering', '-data_emissao')
                contas = contas.order_by(ordering)
                
                page = int(request.GET.get('page', 1))
                page_size = int(request.GET.get('page_size', 20))
                start = (page - 1) * page_size
                end = start + page_size
                
                total = contas.count()
                contas_page = contas[start:end]
                
                serializer = ContaReceberSerializer(contas_page, many=True)
                
                return JsonResponse({
                    'results': serializer.data,
                    'count': total,
                    'previous': f'?page={page-1}' if page > 1 else None,
                    'next': f'?page={page+1}' if end < total else None,
                })
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            data['ativo'] = True
            serializer = ContaReceberSerializer(data=data)
            
            if serializer.is_valid():
                conta = serializer.save()
                return JsonResponse(ContaReceberSerializer(conta).data, status=201)
            else:
                return JsonResponse(serializer.errors, status=400)
        
        elif request.method == 'PUT':
            if not conta_id:
                return JsonResponse({'error': 'ID da conta é obrigatório'}, status=400)
            
            try:
                conta = ContaReceber.objects.get(id=conta_id)
                data = json.loads(request.body)
                serializer = ContaReceberSerializer(conta, data=data, partial=True)
                
                if serializer.is_valid():
                    conta = serializer.save()
                    return JsonResponse(ContaReceberSerializer(conta).data)
                else:
                    return JsonResponse(serializer.errors, status=400)
            except ContaReceber.DoesNotExist:
                return JsonResponse({'error': 'Conta não encontrada'}, status=404)
        
        elif request.method == 'DELETE':
            if not conta_id:
                return JsonResponse({'error': 'ID da conta é obrigatório'}, status=400)
            
            try:
                conta = ContaReceber.objects.get(id=conta_id)
                conta.ativo = False
                conta.save()
                return JsonResponse({'message': 'Conta inativada com sucesso'})
            except ContaReceber.DoesNotExist:
                return JsonResponse({'error': 'Conta não encontrada'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def conta_receber_inativar(request, conta_id):
    try:
        conta = ContaReceber.objects.get(id=conta_id)
        conta.ativo = False
        conta.save()
        return JsonResponse(ContaReceberSerializer(conta).data)
    except ContaReceber.DoesNotExist:
        return JsonResponse({'error': 'Conta não encontrada'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def conta_receber_reativar(request, conta_id):
    try:
        conta = ContaReceber.objects.get(id=conta_id)
        conta.ativo = True
        conta.save()
        return JsonResponse(ContaReceberSerializer(conta).data)
    except ContaReceber.DoesNotExist:
        return JsonResponse({'error': 'Conta não encontrada'}, status=404)

