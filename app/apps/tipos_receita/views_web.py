# -*- coding: utf-8 -*-
"""
Views Web do app Tipos de Receita
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
import json

from .models import TipoReceita
from .serializers import TipoReceitaSerializer


def tipos_receita_list(request):
    """View para listagem de tipos de receita"""
    return render(request, 'tipos_receita/list.html', {'page_title': 'Tipos de Receita'})


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def tipos_receita_api(request, tipo_id=None):
    """API para CRUD de tipos de receita"""
    try:
        if request.method == 'GET':
            if tipo_id:
                try:
                    tipo = TipoReceita.objects.get(id=tipo_id)
                    serializer = TipoReceitaSerializer(tipo)
                    return JsonResponse(serializer.data)
                except TipoReceita.DoesNotExist:
                    return JsonResponse({'error': 'Tipo não encontrado'}, status=404)
            else:
                tipos = TipoReceita.objects.all()
                
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
                
                serializer = TipoReceitaSerializer(tipos_page, many=True)
                
                return JsonResponse({
                    'results': serializer.data,
                    'count': total,
                    'previous': f'?page={page-1}' if page > 1 else None,
                    'next': f'?page={page+1}' if end < total else None,
                })
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            data['ativo'] = True
            serializer = TipoReceitaSerializer(data=data)
            
            if serializer.is_valid():
                tipo = serializer.save()
                return JsonResponse(TipoReceitaSerializer(tipo).data, status=201)
            else:
                return JsonResponse(serializer.errors, status=400)
        
        elif request.method == 'PUT':
            if not tipo_id:
                return JsonResponse({'error': 'ID do tipo é obrigatório'}, status=400)
            
            try:
                tipo = TipoReceita.objects.get(id=tipo_id)
                data = json.loads(request.body)
                serializer = TipoReceitaSerializer(tipo, data=data, partial=True)
                
                if serializer.is_valid():
                    tipo = serializer.save()
                    return JsonResponse(TipoReceitaSerializer(tipo).data)
                else:
                    return JsonResponse(serializer.errors, status=400)
            except TipoReceita.DoesNotExist:
                return JsonResponse({'error': 'Tipo não encontrado'}, status=404)
        
        elif request.method == 'DELETE':
            if not tipo_id:
                return JsonResponse({'error': 'ID do tipo é obrigatório'}, status=400)
            
            try:
                tipo = TipoReceita.objects.get(id=tipo_id)
                tipo.ativo = False
                tipo.save()
                return JsonResponse({'message': 'Tipo inativado com sucesso'})
            except TipoReceita.DoesNotExist:
                return JsonResponse({'error': 'Tipo não encontrado'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def tipo_receita_inativar(request, tipo_id):
    try:
        tipo = TipoReceita.objects.get(id=tipo_id)
        tipo.ativo = False
        tipo.save()
        return JsonResponse(TipoReceitaSerializer(tipo).data)
    except TipoReceita.DoesNotExist:
        return JsonResponse({'error': 'Tipo não encontrado'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def tipo_receita_reativar(request, tipo_id):
    try:
        tipo = TipoReceita.objects.get(id=tipo_id)
        tipo.ativo = True
        tipo.save()
        return JsonResponse(TipoReceitaSerializer(tipo).data)
    except TipoReceita.DoesNotExist:
        return JsonResponse({'error': 'Tipo não encontrado'}, status=404)

