# -*- coding: utf-8 -*-
"""
Views Web do app Faturados
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
import json

from .models import Faturado
from .serializers import FaturadoSerializer


def faturados_list(request):
    """View para listagem de faturados"""
    return render(request, 'faturados/list.html', {'page_title': 'Faturados'})


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def faturados_api(request, faturado_id=None):
    """API para CRUD de faturados"""
    try:
        if request.method == 'GET':
            if faturado_id:
                try:
                    faturado = Faturado.objects.get(id=faturado_id)
                    serializer = FaturadoSerializer(faturado)
                    return JsonResponse(serializer.data)
                except Faturado.DoesNotExist:
                    return JsonResponse({'error': 'Faturado não encontrado'}, status=404)
            else:
                faturados = Faturado.objects.all()
                
                ativo = request.GET.get('ativo')
                if ativo is not None:
                    faturados = faturados.filter(ativo=ativo.lower() == 'true')
                
                search = request.GET.get('search')
                if search:
                    faturados = faturados.filter(
                        Q(nome_completo__icontains=search) | Q(cpf__icontains=search) | Q(email__icontains=search)
                    )
                
                ordering = request.GET.get('ordering', 'nome_completo')
                faturados = faturados.order_by(ordering)
                
                page = int(request.GET.get('page', 1))
                page_size = int(request.GET.get('page_size', 20))
                start = (page - 1) * page_size
                end = start + page_size
                
                total = faturados.count()
                faturados_page = faturados[start:end]
                
                serializer = FaturadoSerializer(faturados_page, many=True)
                
                return JsonResponse({
                    'results': serializer.data,
                    'count': total,
                    'previous': f'?page={page-1}' if page > 1 else None,
                    'next': f'?page={page+1}' if end < total else None,
                })
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            data['ativo'] = True
            serializer = FaturadoSerializer(data=data)
            
            if serializer.is_valid():
                faturado = serializer.save()
                return JsonResponse(FaturadoSerializer(faturado).data, status=201)
            else:
                return JsonResponse(serializer.errors, status=400)
        
        elif request.method == 'PUT':
            if not faturado_id:
                return JsonResponse({'error': 'ID do faturado é obrigatório'}, status=400)
            
            try:
                faturado = Faturado.objects.get(id=faturado_id)
                data = json.loads(request.body)
                serializer = FaturadoSerializer(faturado, data=data, partial=True)
                
                if serializer.is_valid():
                    faturado = serializer.save()
                    return JsonResponse(FaturadoSerializer(faturado).data)
                else:
                    return JsonResponse(serializer.errors, status=400)
            except Faturado.DoesNotExist:
                return JsonResponse({'error': 'Faturado não encontrado'}, status=404)
        
        elif request.method == 'DELETE':
            if not faturado_id:
                return JsonResponse({'error': 'ID do faturado é obrigatório'}, status=400)
            
            try:
                faturado = Faturado.objects.get(id=faturado_id)
                faturado.ativo = False
                faturado.save()
                return JsonResponse({'message': 'Faturado inativado com sucesso'})
            except Faturado.DoesNotExist:
                return JsonResponse({'error': 'Faturado não encontrado'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def faturado_inativar(request, faturado_id):
    try:
        faturado = Faturado.objects.get(id=faturado_id)
        faturado.ativo = False
        faturado.save()
        return JsonResponse(FaturadoSerializer(faturado).data)
    except Faturado.DoesNotExist:
        return JsonResponse({'error': 'Faturado não encontrado'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def faturado_reativar(request, faturado_id):
    try:
        faturado = Faturado.objects.get(id=faturado_id)
        faturado.ativo = True
        faturado.save()
        return JsonResponse(FaturadoSerializer(faturado).data)
    except Faturado.DoesNotExist:
        return JsonResponse({'error': 'Faturado não encontrado'}, status=404)

