# -*- coding: utf-8 -*-
"""
Views Web do app Processador de PDF
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db import transaction
import json

from .models import ProcessamentoPDF
from apps.fornecedores.models import Fornecedor


def pdf_processor_list(request):
    """
    View para listagem de processamentos de PDF
    """
    context = {
        'page_title': 'Processar PDF',
        'user': request.user,
    }
    return render(request, 'pdf_processor/list.html', context)


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def pdf_processor_api(request, processamento_id=None):
    """
    API para CRUD de processamentos de PDF
    """
    try:
        if request.method == 'GET':
            if processamento_id:
                # Buscar processamento específico
                try:
                    processamento = ProcessamentoPDF.objects.get(id=processamento_id, ativo=True)
                    return JsonResponse({
                        'id': processamento.id,
                        'nome_arquivo': processamento.nome_arquivo,
                        'tamanho_arquivo': processamento.tamanho_arquivo,
                        'status_processamento': processamento.status_processamento,
                        'status_display': processamento.get_status_processamento_display(),
                        'dados_extraidos': processamento.dados_extraidos,
                        'erro_processamento': processamento.erro_processamento,
                        'data_processamento': processamento.data_processamento.isoformat() if processamento.data_processamento else None,
                        'tempo_processamento': processamento.tempo_processamento.total_seconds() if processamento.tempo_processamento else None,
                        'ativo': processamento.ativo,
                        'criado_em': processamento.criado_em.isoformat(),
                    })
                except ProcessamentoPDF.DoesNotExist:
                    return JsonResponse({'error': 'Processamento não encontrado'}, status=404)
            else:
                # Listar processamentos
                processamentos = ProcessamentoPDF.objects.filter(ativo=True)
                
                # Filtros
                status = request.GET.get('status_processamento')
                if status:
                    processamentos = processamentos.filter(status_processamento=status)
                
                search = request.GET.get('search')
                if search:
                    processamentos = processamentos.filter(
                        nome_arquivo__icontains=search
                    )
                
                # Ordenação
                ordering = request.GET.get('ordering', '-criado_em')
                processamentos = processamentos.order_by(ordering)
                
                # Paginação
                page = int(request.GET.get('page', 1))
                page_size = int(request.GET.get('page_size', 20))
                start = (page - 1) * page_size
                end = start + page_size
                
                total = processamentos.count()
                processamentos_page = processamentos[start:end]
                
                # Serializar manualmente para evitar problemas
                results = []
                for p in processamentos_page:
                    results.append({
                        'id': p.id,
                        'nome_arquivo': p.nome_arquivo,
                        'tamanho_arquivo': p.tamanho_arquivo,
                        'status_processamento': p.status_processamento,
                        'status_display': p.get_status_processamento_display(),
                        'data_processamento': p.data_processamento.isoformat() if p.data_processamento else None,
                        'ativo': p.ativo,
                        'criado_em': p.criado_em.isoformat(),
                    })
                
                return JsonResponse({
                    'results': results,
                    'count': total,
                    'previous': f'/pdf-processor/api/?page={page-1}' if page > 1 else None,
                    'next': f'/pdf-processor/api/?page={page+1}' if end < total else None,
                })
        
        elif request.method == 'POST':
            # Criar processamento
            data = json.loads(request.body)
            try:
                processamento = ProcessamentoPDF.objects.create(
                    nome_arquivo=data.get('nome_arquivo', ''),
                    tamanho_arquivo=data.get('tamanho_arquivo', 0),
                    status_processamento=data.get('status_processamento', 'PENDENTE')
                )
                return JsonResponse({
                    'id': processamento.id,
                    'nome_arquivo': processamento.nome_arquivo,
                    'status_processamento': processamento.status_processamento,
                    'criado_em': processamento.criado_em.isoformat(),
                }, status=201)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        
        elif request.method == 'PUT':
            # Atualizar processamento
            if not processamento_id:
                return JsonResponse({'error': 'ID do processamento é obrigatório'}, status=400)
            
            try:
                processamento = ProcessamentoPDF.objects.get(id=processamento_id)
                data = json.loads(request.body)
                
                # Atualizar campos se fornecidos
                if 'nome_arquivo' in data:
                    processamento.nome_arquivo = data['nome_arquivo']
                if 'status_processamento' in data:
                    processamento.status_processamento = data['status_processamento']
                if 'dados_extraidos' in data:
                    processamento.dados_extraidos = data['dados_extraidos']
                if 'erro_processamento' in data:
                    processamento.erro_processamento = data['erro_processamento']
                
                processamento.save()
                
                return JsonResponse({
                    'id': processamento.id,
                    'nome_arquivo': processamento.nome_arquivo,
                    'status_processamento': processamento.status_processamento,
                    'dados_extraidos': processamento.dados_extraidos,
                    'erro_processamento': processamento.erro_processamento,
                    'atualizado_em': processamento.atualizado_em.isoformat(),
                })
            except ProcessamentoPDF.DoesNotExist:
                return JsonResponse({'error': 'Processamento não encontrado'}, status=404)
        
        elif request.method == 'DELETE':
            # Excluir processamento
            if not processamento_id:
                return JsonResponse({'error': 'ID do processamento é obrigatório'}, status=400)
            
            try:
                processamento = ProcessamentoPDF.objects.get(id=processamento_id)
                processamento.delete()
                return JsonResponse({'message': 'Processamento excluído com sucesso'})
            except ProcessamentoPDF.DoesNotExist:
                return JsonResponse({'error': 'Processamento não encontrado'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def pdf_processor_reprocessar(request, processamento_id):
    """
    Reprocessar PDF
    """
    try:
        processamento = ProcessamentoPDF.objects.get(id=processamento_id)
        
        # Reset do status
        processamento.status_processamento = 'PENDENTE'
        processamento.erro_processamento = None
        processamento.dados_extraidos = None
        processamento.data_processamento = None
        processamento.tempo_processamento = None
        processamento.save()
        
        # Aqui seria chamado o processamento assíncrono
        # Por enquanto, apenas simula
        processamento.iniciar_processamento()
        
        return JsonResponse({
            'id': processamento.id,
            'nome_arquivo': processamento.nome_arquivo,
            'status_processamento': processamento.status_processamento,
            'status_display': processamento.get_status_processamento_display(),
            'atualizado_em': processamento.atualizado_em.isoformat(),
        })
    except ProcessamentoPDF.DoesNotExist:
        return JsonResponse({'error': 'Processamento não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def pdf_processor_upload(request):
    """
    Upload e processamento de PDF
    """
    try:
        if 'arquivo_pdf' not in request.FILES:
            return JsonResponse({'error': 'Arquivo PDF é obrigatório'}, status=400)
        
        arquivo = request.FILES['arquivo_pdf']
        
        # Validar arquivo
        if not arquivo.name.lower().endswith('.pdf'):
            return JsonResponse({'error': 'Apenas arquivos PDF são permitidos'}, status=400)
        
        if arquivo.size > 16 * 1024 * 1024:  # 16MB
            return JsonResponse({'error': 'Arquivo muito grande. Máximo 16MB'}, status=400)
        
        # Criar registro de processamento
        processamento = ProcessamentoPDF.objects.create(
            arquivo_pdf=arquivo,
            nome_arquivo=arquivo.name,
            tamanho_arquivo=arquivo.size
        )
        
        # Simular processamento (aqui seria integrado com Gemini)
        processamento.iniciar_processamento()
        
        # Simular dados extraídos
        dados_extraidos = {
            'fornecedor': {
                'razao_social': 'Fornecedor Exemplo Ltda',
                'cnpj': '12.345.678/0001-90',
                'email': 'contato@exemplo.com'
            },
            'faturado': {
                'nome_completo': 'João Silva',
                'cpf': '123.456.789-00'
            },
            'nota_fiscal': {
                'numero': '12345',
                'data_emissao': '2024-01-15',
                'valor_total': 1500.00,
                'descricao': 'Produtos agrícolas'
            },
            'parcelas': [
                {
                    'numero': 1,
                    'data_vencimento': '2024-02-15',
                    'valor': 750.00
                },
                {
                    'numero': 2,
                    'data_vencimento': '2024-03-15',
                    'valor': 750.00
                }
            ],
            'classificacao': {
                'tipo_despesa': 'INSUMOS_AGRICOLAS',
                'confianca': 0.85
            }
        }
        
        # Finalizar processamento
        from django.utils import timezone
        import datetime
        tempo_processamento = datetime.timedelta(seconds=2.5)
        processamento.finalizar_processamento(
            dados_extraidos=dados_extraidos,
            tempo_processamento=tempo_processamento
        )
        
        return JsonResponse({
            'id': processamento.id,
            'nome_arquivo': processamento.nome_arquivo,
            'tamanho_arquivo': processamento.tamanho_arquivo,
            'status_processamento': processamento.status_processamento,
            'status_display': processamento.get_status_processamento_display(),
            'dados_extraidos': processamento.dados_extraidos,
            'data_processamento': processamento.data_processamento.isoformat() if processamento.data_processamento else None,
            'criado_em': processamento.criado_em.isoformat(),
        }, status=201)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def pdf_processed_list(request):
    """
    View para listar PDFs processados com sucesso
    """
    context = {
        'page_title': 'PDFs Processados',
        'user': request.user,
    }
    return render(request, 'pdf_processor/processed_list.html', context)


def pdf_processed_detail(request, processamento_id):
    """
    View para mostrar detalhes de um PDF processado
    """
    processamento = get_object_or_404(ProcessamentoPDF, id=processamento_id, ativo=True)
    
    # Verificar se o processamento foi bem-sucedido
    if not processamento.is_sucesso():
        messages.error(request, 'Este PDF não foi processado com sucesso.')
        return render(request, 'pdf_processor/processed_list.html')
    
    # Obter dados extraídos
    dados_extraidos = processamento.dados_extraidos or {}
    
    # Verificar fornecedor no banco
    fornecedor_info = verificar_fornecedor_no_banco(dados_extraidos.get('fornecedor', {}))
    
    # Verificar faturado no banco
    faturado_info = verificar_faturado_no_banco(dados_extraidos.get('cliente', {}))
    
    # Verificar classificação de despesa
    despesa_info = verificar_despesa_no_banco(dados_extraidos.get('classificacao_geral', ''))
    
    context = {
        'page_title': f'Detalhes - {processamento.nome_arquivo}',
        'user': request.user,
        'processamento': processamento,
        'dados_extraidos': dados_extraidos,
        'fornecedor_info': fornecedor_info,
        'faturado_info': faturado_info,
        'despesa_info': despesa_info,
    }
    return render(request, 'pdf_processor/processed_detail.html', context)


def verificar_fornecedor_no_banco(dados_fornecedor):
    """
    Verifica se o fornecedor já existe no banco de dados
    """
    if not dados_fornecedor:
        return {'existe': False, 'mensagem': 'NÃO EXISTE'}
    
    cnpj = dados_fornecedor.get('cnpj', '')
    nome = dados_fornecedor.get('nome', '')
    
    # Buscar por CNPJ primeiro
    if cnpj:
        try:
            fornecedor = Fornecedor.objects.get(cnpj=cnpj, ativo=True)
            return {
                'existe': True, 
                'id': fornecedor.id,
                'mensagem': f'EXISTE – ID: {fornecedor.id}',
            }
        except Fornecedor.DoesNotExist:
            pass
    
    # Buscar por nome se CNPJ não encontrado
    if nome:
        try:
            fornecedor = Fornecedor.objects.get(razao_social__icontains=nome, ativo=True)
            return {
                'existe': True, 
                'id': fornecedor.id,
                'mensagem': f'EXISTE – ID: {fornecedor.id}',
            }
        except Fornecedor.DoesNotExist:
            pass
    
    return {'existe': False, 'mensagem': 'NÃO EXISTE'}


def verificar_processamento_duplicado(dados_extraidos):
    """
    Verifica se já existe um processamento similar no banco
    """
    if not dados_extraidos:
        return None
    
    # Buscar por dados similares
    fornecedor = dados_extraidos.get('fornecedor', {})
    cliente = dados_extraidos.get('cliente', {})
    nota_fiscal = dados_extraidos.get('nota_fiscal', {})
    
    # Critérios de busca
    criterios = {}
    
    # Por CNPJ do fornecedor
    if fornecedor.get('cnpj'):
        criterios['dados_extraidos__fornecedor__cnpj'] = fornecedor['cnpj']
    
    # Por CPF do cliente
    if cliente.get('cpf'):
        criterios['dados_extraidos__cliente__cpf'] = cliente['cpf']
    
    # Por número da nota fiscal
    if nota_fiscal.get('numero'):
        criterios['dados_extraidos__nota_fiscal__numero'] = nota_fiscal['numero']
    
    # Se não há critérios suficientes, não verificar duplicata
    if not criterios:
        return None
    
    try:
        # Buscar processamento similar
        processamento_similar = ProcessamentoPDF.objects.filter(
            status_processamento='SUCESSO',
            ativo=True,
            **criterios
        ).first()
        
        return processamento_similar
    except Exception:
        return None


def verificar_faturado_no_banco(dados_faturado):
    """
    Verifica se o faturado já existe no banco de dados
    """
    from apps.faturados.models import Faturado
    
    if not dados_faturado:
        return {'existe': False, 'mensagem': 'NÃO EXISTE'}
    
    cpf = dados_faturado.get('cpf', '')
    nome = dados_faturado.get('nome', '')
    
    # Buscar por CPF primeiro
    if cpf:
        try:
            faturado = Faturado.objects.get(cpf=cpf, ativo=True)
            return {
                'existe': True, 
                'id': faturado.id,
                'mensagem': f'EXISTE – ID: {faturado.id}',
            }
        except Faturado.DoesNotExist:
            pass
    
    # Buscar por nome se CPF não encontrado
    if nome:
        try:
            faturado = Faturado.objects.get(nome_completo__icontains=nome, ativo=True)
            return {
                'existe': True, 
                'id': faturado.id,
                'mensagem': f'EXISTE – ID: {faturado.id}',
            }
        except Faturado.DoesNotExist:
            pass
    
    return {'existe': False, 'mensagem': 'NÃO EXISTE'}


def verificar_despesa_no_banco(classificacao):
    """
    Verifica se a classificação de despesa já existe no banco
    """
    from apps.tipos_despesa.models import TipoDespesa
    
    if not classificacao:
        return {'existe': False, 'mensagem': 'NÃO EXISTE'}
    
    # Buscar por nome exato
    try:
        tipo_despesa = TipoDespesa.objects.get(nome__iexact=classificacao, ativo=True)
        return {
            'existe': True, 
            'id': tipo_despesa.id,
            'mensagem': f'EXISTE – ID: {tipo_despesa.id}',
            'tipo_despesa': tipo_despesa
        }
    except TipoDespesa.DoesNotExist:
        pass
    
    # Buscar por nome similar
    try:
        tipo_despesa = TipoDespesa.objects.filter(nome__icontains=classificacao, ativo=True).first()
        if tipo_despesa:
            return {
                'existe': True, 
                'id': tipo_despesa.id,
                'mensagem': f'EXISTE – ID: {tipo_despesa.id}',
            }
    except Exception:
        pass
    
    return {'existe': False, 'mensagem': 'NÃO EXISTE'}


@csrf_exempt
@require_http_methods(["POST"])
def criar_registros_banco(request, processamento_id):
    """
    Cria registros no banco de dados baseado nos dados extraídos
    Implementa lógica de IDs condicionais para evitar duplicatas
    """
    try:
        processamento = get_object_or_404(ProcessamentoPDF, id=processamento_id, ativo=True)
        dados_extraidos = processamento.dados_extraidos or {}
        
        # Verificar se já existe processamento similar
        processamento_similar = verificar_processamento_duplicado(dados_extraidos)
        
        registros_criados = []
        mensagem_status = []
        
        if processamento_similar and processamento_similar.id != processamento.id:
            # Se existe processamento similar, não criar novos registros
            mensagem_status.append(f'Processamento similar já existe - ID: {processamento_similar.id}')
            
            # Atualizar status do processamento atual
            processamento.status_processamento = 'DUPLICADO'
            processamento.erro_processamento = f'Processamento duplicado. Original: ID {processamento_similar.id}'
            processamento.save()
            
            return JsonResponse({
                'success': True,
                'duplicado': True,
                'processamento_original_id': processamento_similar.id,
                'mensagem': 'Processamento duplicado detectado. Não foram criados novos registros.',
                'registros_criados': []
            })
        
        # Se não é duplicata, proceder com criação de registros
        with transaction.atomic():
            # Criar fornecedor se não existir
            dados_fornecedor = dados_extraidos.get('fornecedor', {})
            if dados_fornecedor:
                fornecedor_info = verificar_fornecedor_no_banco(dados_fornecedor)
                
                if not fornecedor_info['existe']:
                    # Criar novo fornecedor
                    fornecedor = Fornecedor.objects.create(
                        razao_social=dados_fornecedor.get('nome', 'Nome não informado'),
                        cnpj=dados_fornecedor.get('cnpj', '00.000.000/0000-00'),
                        email=dados_fornecedor.get('email', ''),
                        endereco=dados_fornecedor.get('endereco', ''),
                    )
                    registros_criados.append(f'Fornecedor criado - ID: {fornecedor.id}')
                    mensagem_status.append(f'FORNECEDOR CRIADO – ID: {fornecedor.id}')
                else:
                    mensagem_status.append(f'FORNECEDOR EXISTE – ID: {fornecedor_info["id"]}')
            
            # Funcionalidades de faturado e despesa removidas para simplificação
        
        if registros_criados:
            messages.success(request, f'Registros criados com sucesso: {", ".join(registros_criados)}')
        else:
            messages.info(request, 'Todos os registros já existem no banco de dados.')
        
        return JsonResponse({
            'success': True,
            'duplicado': False,
            'registros_criados': registros_criados,
            'mensagem_status': mensagem_status
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

