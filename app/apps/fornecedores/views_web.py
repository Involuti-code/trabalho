# -*- coding: utf-8 -*-
"""
Views Web do app Fornecedores
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .models import Fornecedor
from .serializers import FornecedorSerializer, FornecedorListSerializer


def fornecedores_list(request):
    """
    View para listagem de fornecedores
    """
    context = {
        'page_title': 'Fornecedores',
        'user': request.user,
    }
    return render(request, 'fornecedores/list.html', context)


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def fornecedores_api(request, fornecedor_id=None):
    """
    API para CRUD de fornecedores
    """
    try:
        if request.method == 'GET':
            if fornecedor_id:
                # Buscar fornecedor específico
                try:
                    fornecedor = Fornecedor.objects.get(id=fornecedor_id, ativo=True)
                    serializer = FornecedorSerializer(fornecedor)
                    return JsonResponse(serializer.data)
                except Fornecedor.DoesNotExist:
                    return JsonResponse({'error': 'Fornecedor não encontrado'}, status=404)
            else:
                # Listar fornecedores
                fornecedores = Fornecedor.objects.all()
                
                # Filtros
                ativo = request.GET.get('ativo')
                if ativo is not None:
                    fornecedores = fornecedores.filter(ativo=ativo.lower() == 'true')
                
                search = request.GET.get('search')
                if search:
                    fornecedores = fornecedores.filter(
                        razao_social__icontains=search
                    ) | fornecedores.filter(
                        fantasia__icontains=search
                    ) | fornecedores.filter(
                        cnpj__icontains=search
                    )
                
                # Ordenação
                ordering = request.GET.get('ordering', 'razao_social')
                fornecedores = fornecedores.order_by(ordering)
                
                # Paginação
                page = int(request.GET.get('page', 1))
                page_size = int(request.GET.get('page_size', 20))
                start = (page - 1) * page_size
                end = start + page_size
                
                total = fornecedores.count()
                fornecedores_page = fornecedores[start:end]
                
                serializer = FornecedorListSerializer(fornecedores_page, many=True)
                
                return JsonResponse({
                    'results': serializer.data,
                    'count': total,
                    'previous': f'/api/fornecedores/?page={page-1}' if page > 1 else None,
                    'next': f'/api/fornecedores/?page={page+1}' if end < total else None,
                })
        
        elif request.method == 'POST':
            # Criar fornecedor
            data = json.loads(request.body)
            serializer = FornecedorSerializer(data=data)
            
            if serializer.is_valid():
                fornecedor = serializer.save()
                return JsonResponse(FornecedorSerializer(fornecedor).data, status=201)
            else:
                return JsonResponse(serializer.errors, status=400)
        
        elif request.method == 'PUT':
            # Atualizar fornecedor
            if not fornecedor_id:
                return JsonResponse({'error': 'ID do fornecedor é obrigatório'}, status=400)
            
            try:
                fornecedor = Fornecedor.objects.get(id=fornecedor_id)
                data = json.loads(request.body)
                serializer = FornecedorSerializer(fornecedor, data=data, partial=True)
                
                if serializer.is_valid():
                    fornecedor = serializer.save()
                    return JsonResponse(FornecedorSerializer(fornecedor).data)
                else:
                    return JsonResponse(serializer.errors, status=400)
            except Fornecedor.DoesNotExist:
                return JsonResponse({'error': 'Fornecedor não encontrado'}, status=404)
        
        elif request.method == 'DELETE':
            # Excluir fornecedor
            if not fornecedor_id:
                return JsonResponse({'error': 'ID do fornecedor é obrigatório'}, status=400)
            
            try:
                fornecedor = Fornecedor.objects.get(id=fornecedor_id)
                fornecedor.delete()
                return JsonResponse({'message': 'Fornecedor excluído com sucesso'})
            except Fornecedor.DoesNotExist:
                return JsonResponse({'error': 'Fornecedor não encontrado'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def fornecedor_inativar(request, fornecedor_id):
    """
    Inativar fornecedor
    """
    try:
        fornecedor = Fornecedor.objects.get(id=fornecedor_id)
        fornecedor.inativar()
        serializer = FornecedorSerializer(fornecedor)
        return JsonResponse(serializer.data)
    except Fornecedor.DoesNotExist:
        return JsonResponse({'error': 'Fornecedor não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def fornecedor_reativar(request, fornecedor_id):
    """
    Reativar fornecedor
    """
    try:
        fornecedor = Fornecedor.objects.get(id=fornecedor_id)
        fornecedor.reativar()
        serializer = FornecedorSerializer(fornecedor)
        return JsonResponse(serializer.data)
    except Fornecedor.DoesNotExist:
        return JsonResponse({'error': 'Fornecedor não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

