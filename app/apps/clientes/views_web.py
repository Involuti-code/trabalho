# -*- coding: utf-8 -*-
"""
Views Web do app Clientes
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
import json

from .models import Cliente
from .serializers import ClienteSerializer


def clientes_list(request):
    """View para listagem de clientes"""
    return render(request, 'clientes/list.html', {'page_title': 'Clientes'})


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def clientes_api(request, cliente_id=None):
    """API para CRUD de clientes"""
    try:
        if request.method == 'GET':
            if cliente_id:
                try:
                    cliente = Cliente.objects.get(id=cliente_id)
                    serializer = ClienteSerializer(cliente)
                    return JsonResponse(serializer.data)
                except Cliente.DoesNotExist:
                    return JsonResponse({'error': 'Cliente não encontrado'}, status=404)
            else:
                clientes = Cliente.objects.all()
                
                # Filtro por status
                ativo = request.GET.get('ativo')
                if ativo is not None:
                    clientes = clientes.filter(ativo=ativo.lower() == 'true')
                
                # Busca
                search = request.GET.get('search')
                if search:
                    clientes = clientes.filter(
                        Q(nome__icontains=search) | Q(cpf__icontains=search) | Q(email__icontains=search)
                    )
                
                # Ordenação
                ordering = request.GET.get('ordering', 'nome')
                clientes = clientes.order_by(ordering)
                
                # Paginação
                page = int(request.GET.get('page', 1))
                page_size = int(request.GET.get('page_size', 20))
                start = (page - 1) * page_size
                end = start + page_size
                
                total = clientes.count()
                clientes_page = clientes[start:end]
                
                serializer = ClienteSerializer(clientes_page, many=True)
                
                return JsonResponse({
                    'results': serializer.data,
                    'count': total,
                    'previous': f'?page={page-1}' if page > 1 else None,
                    'next': f'?page={page+1}' if end < total else None,
                })
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            data['ativo'] = True  # STATUS oculto == ATIVO no CREATE
            serializer = ClienteSerializer(data=data)
            
            if serializer.is_valid():
                cliente = serializer.save()
                return JsonResponse(ClienteSerializer(cliente).data, status=201)
            else:
                return JsonResponse(serializer.errors, status=400)
        
        elif request.method == 'PUT':
            if not cliente_id:
                return JsonResponse({'error': 'ID do cliente é obrigatório'}, status=400)
            
            try:
                cliente = Cliente.objects.get(id=cliente_id)
                data = json.loads(request.body)
                serializer = ClienteSerializer(cliente, data=data, partial=True)
                
                if serializer.is_valid():
                    cliente = serializer.save()
                    return JsonResponse(ClienteSerializer(cliente).data)
                else:
                    return JsonResponse(serializer.errors, status=400)
            except Cliente.DoesNotExist:
                return JsonResponse({'error': 'Cliente não encontrado'}, status=404)
        
        elif request.method == 'DELETE':
            # DELETE lógico - altera STATUS == INATIVO
            if not cliente_id:
                return JsonResponse({'error': 'ID do cliente é obrigatório'}, status=400)
            
            try:
                cliente = Cliente.objects.get(id=cliente_id)
                cliente.ativo = False
                cliente.save()
                return JsonResponse({'message': 'Cliente inativado com sucesso'})
            except Cliente.DoesNotExist:
                return JsonResponse({'error': 'Cliente não encontrado'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def cliente_inativar(request, cliente_id):
    """Inativar cliente"""
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        cliente.ativo = False
        cliente.save()
        return JsonResponse(ClienteSerializer(cliente).data)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def cliente_reativar(request, cliente_id):
    """Reativar cliente"""
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        cliente.ativo = True
        cliente.save()
        return JsonResponse(ClienteSerializer(cliente).data)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)

