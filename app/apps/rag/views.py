# -*- coding: utf-8 -*-
"""
Views do app RAG
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json

from .services import RAGSimpleService, RAGEmbeddingsService
from .models import ConsultaRAG


class RAGView(View):
    """
    View principal para interface RAG
    """
    
    def get(self, request):
        """Renderiza a página de consulta RAG"""
        return render(request, 'rag/index.html')


@method_decorator(csrf_exempt, name='dispatch')
class ConsultarRAGView(View):
    """
    View para processar consultas RAG
    """
    
    def post(self, request):
        """Processa uma consulta RAG"""
        try:
            data = json.loads(request.body)
            pergunta = data.get('pergunta', '').strip()
            tipo_rag = data.get('tipo_rag', 'SIMPLES')
            
            if not pergunta:
                return JsonResponse({
                    'success': False,
                    'error': 'Pergunta não fornecida'
                }, status=400)
            
            # Processar consulta
            if tipo_rag == 'EMBEDDINGS':
                service = RAGEmbeddingsService()
            else:
                service = RAGSimpleService()
            
            resultado = service.processar_consulta(pergunta)
            
            # Salvar consulta no banco de dados
            if resultado.get('success'):
                ConsultaRAG.objects.create(
                    pergunta=pergunta,
                    tipo_rag=tipo_rag,
                    contexto_retornado=resultado.get('contexto', '')[:5000],  # Limitar tamanho
                    resposta_llm=resultado.get('resposta', ''),
                    tempo_resposta=resultado.get('tempo_resposta', 0)
                )
            
            return JsonResponse(resultado)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'JSON inválido'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class HistoricoRAGView(View):
    """
    View para obter histórico de consultas RAG
    """
    
    def get(self, request):
        """Retorna histórico de consultas"""
        try:
            limite = int(request.GET.get('limite', 10))
            consultas = ConsultaRAG.objects.filter(ativo=True).order_by('-criado_em')[:limite]
            
            dados = []
            for consulta in consultas:
                dados.append({
                    'id': consulta.id,
                    'pergunta': consulta.pergunta,
                    'tipo_rag': consulta.tipo_rag,
                    'resposta': consulta.resposta_llm[:500] + '...' if consulta.resposta_llm and len(consulta.resposta_llm) > 500 else consulta.resposta_llm,
                    'tempo_resposta': consulta.tempo_resposta,
                    'criado_em': consulta.criado_em.strftime('%d/%m/%Y %H:%M:%S')
                })
            
            return JsonResponse({
                'success': True,
                'consultas': dados
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

