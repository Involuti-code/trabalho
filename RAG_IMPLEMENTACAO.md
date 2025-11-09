# Implementação RAG - Busca Inteligente

## Resumo da Implementação

Foi implementado um sistema completo de RAG (Retrieval-Augmented Generation) com duas modalidades:

### 1. RAG Simples
- **Funcionalidade**: Busca por palavras-chave no banco de dados
- **Como funciona**: 
  - Divide a pergunta em palavras-chave
  - Busca em todas as tabelas (Clientes, Fornecedores, Contas a Pagar, Contas a Receber)
  - Retorna resultados que contenham as palavras-chave
  - Envia contexto para o LLM (Gemini) gerar resposta elaborada

### 2. RAG com Embeddings
- **Funcionalidade**: Busca semântica usando embeddings
- **Como funciona**:
  - Gera embeddings da pergunta usando sentence-transformers
  - Gera embeddings de todos os registros do banco de dados
  - Calcula similaridade de cosseno entre embeddings
  - Retorna resultados ordenados por relevância semântica
  - Envia contexto para o LLM (Gemini) gerar resposta elaborada
  - **Fallback**: Se sentence-transformers não estiver disponível, usa RAG Simples

## Estrutura Criada

### App Django: `apps.rag`
- **Models**: `ConsultaRAG` - Armazena histórico de consultas
- **Services**: 
  - `GeminiService` - Integração com API Gemini
  - `RAGSimpleService` - Implementação RAG simples
  - `RAGEmbeddingsService` - Implementação RAG com embeddings
- **Views**: 
  - `RAGView` - Interface principal
  - `ConsultarRAGView` - Processa consultas
  - `HistoricoRAGView` - Retorna histórico
- **Templates**: Interface web moderna e responsiva
- **URLs**: `/rag/` - Acesso à interface

## Funcionalidades

1. **Interface Web**:
   - Seleção de tipo de RAG (Simples ou Embeddings)
   - Campo para digitar perguntas
   - Exibição de respostas elaboradas pelo LLM
   - Exibição de contexto utilizado
   - Histórico de consultas realizadas
   - Tempo de resposta

2. **Integração com Banco de Dados**:
   - Busca em Clientes
   - Busca em Fornecedores
   - Busca em Contas a Pagar
   - Busca em Contas a Receber

3. **Integração com LLM**:
   - Usa a mesma API Gemini já configurada no projeto
   - Gera respostas elaboradas baseadas no contexto do banco de dados
   - Prompt otimizado para análise financeira e administrativa

## Dependências Adicionadas

- `sentence-transformers==2.2.2` - Para geração de embeddings
- `torch==2.0.1` - Dependência do sentence-transformers

## Como Usar

1. **Acessar a interface**: `http://localhost:8000/rag/`
2. **Selecionar tipo de RAG**: Simples ou Embeddings
3. **Digitar pergunta**: Ex: "Quais são os fornecedores cadastrados?"
4. **Enviar**: O sistema busca no banco de dados e gera resposta elaborada

## Exemplos de Perguntas

- "Quais são os fornecedores cadastrados?"
- "Quais contas estão pendentes?"
- "Quanto devemos receber este mês?"
- "Quais clientes têm contas vencidas?"
- "Qual o total de contas a pagar?"

## Configuração

O sistema está configurado para usar a mesma API Gemini já existente no projeto:
- API Key: Configurada em `gemini_service.py`
- Modelo: `gemini-2.0-flash`

## Notas Importantes

1. **RAG com Embeddings**: Requer instalação de `sentence-transformers` e `torch` (pode ser pesado)
2. **Fallback Automático**: Se embeddings não estiverem disponíveis, usa RAG Simples
3. **Performance**: RAG Simples é mais rápido, RAG Embeddings é mais preciso semanticamente
4. **Histórico**: Todas as consultas são salvas no banco de dados para análise posterior

## Próximos Passos (Opcional)

- Cache de embeddings para melhorar performance
- Indexação de embeddings no banco de dados
- Suporte a mais tabelas
- Análise de sentimentos
- Exportação de relatórios baseados em consultas

