# -*- coding: utf-8 -*-
"""
Views Web do app Tipos de Despesa
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
import json

from .models import TipoDespesa
from .serializers import TipoDespesaSerializer
from apps.core.models import CategoriaDespesa


def tipos_despesa_list(request):
    """View para listagem de tipos de despesa"""
    categorias = [(c.value, c.label) for c in CategoriaDespesa]
    return render(request, 'tipos_despesa/list.html', {
        'page_title': 'Tipos de Despesa',
        'categorias': categorias,
    })


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def tipos_despesa_api(request, tipo_id=None):
    """API para CRUD de tipos de despesa"""
    try:
        if request.method == 'GET':
            if tipo_id:
                try:
                    tipo = TipoDespesa.objects.get(id=tipo_id)
                    serializer = TipoDespesaSerializer(tipo)
                    return JsonResponse(serializer.data)
                except TipoDespesa.DoesNotExist:
                    return JsonResponse({'error': 'Tipo não encontrado'}, status=404)
            else:
                tipos = TipoDespesa.objects.all()
                
                ativo = request.GET.get('ativo')
                if ativo is not None:
                    tipos = tipos.filter(ativo=ativo.lower() == 'true')
                
                search = request.GET.get('search')
                if search:
                    tipos = tipos.filter(
                        Q(nome__icontains=search) | Q(codigo__icontains=search) | Q(descricao__icontains=search)
                    )
                
                ordering = request.GET.get('ordering', 'nome')
                tipos = tipos.order_by(ordering)
                
                page = int(request.GET.get('page', 1))
                page_size = int(request.GET.get('page_size', 20))
                start = (page - 1) * page_size
                end = start + page_size
                
                total = tipos.count()
                tipos_page = tipos[start:end]
                
                serializer = TipoDespesaSerializer(tipos_page, many=True)
                
                return JsonResponse({
                    'results': serializer.data,
                    'count': total,
                    'previous': f'?page={page-1}' if page > 1 else None,
                    'next': f'?page={page+1}' if end < total else None,
                })
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            data['ativo'] = True
            serializer = TipoDespesaSerializer(data=data)
            
            if serializer.is_valid():
                tipo = serializer.save()
                return JsonResponse(TipoDespesaSerializer(tipo).data, status=201)
            else:
                return JsonResponse(serializer.errors, status=400)
        
        elif request.method == 'PUT':
            if not tipo_id:
                return JsonResponse({'error': 'ID do tipo é obrigatório'}, status=400)
            
            try:
                tipo = TipoDespesa.objects.get(id=tipo_id)
                data = json.loads(request.body)
                serializer = TipoDespesaSerializer(tipo, data=data, partial=True)
                
                if serializer.is_valid():
                    tipo = serializer.save()
                    return JsonResponse(TipoDespesaSerializer(tipo).data)
                else:
                    return JsonResponse(serializer.errors, status=400)
            except TipoDespesa.DoesNotExist:
                return JsonResponse({'error': 'Tipo não encontrado'}, status=404)
        
        elif request.method == 'DELETE':
            if not tipo_id:
                return JsonResponse({'error': 'ID do tipo é obrigatório'}, status=400)
            
            try:
                tipo = TipoDespesa.objects.get(id=tipo_id)
                tipo.ativo = False
                tipo.save()
                return JsonResponse({'message': 'Tipo inativado com sucesso'})
            except TipoDespesa.DoesNotExist:
                return JsonResponse({'error': 'Tipo não encontrado'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def tipo_despesa_inativar(request, tipo_id):
    try:
        tipo = TipoDespesa.objects.get(id=tipo_id)
        tipo.ativo = False
        tipo.save()
        return JsonResponse(TipoDespesaSerializer(tipo).data)
    except TipoDespesa.DoesNotExist:
        return JsonResponse({'error': 'Tipo não encontrado'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def tipo_despesa_reativar(request, tipo_id):
    try:
        tipo = TipoDespesa.objects.get(id=tipo_id)
        tipo.ativo = True
        tipo.save()
        return JsonResponse(TipoDespesaSerializer(tipo).data)
    except TipoDespesa.DoesNotExist:
        return JsonResponse({'error': 'Tipo não encontrado'}, status=404)

