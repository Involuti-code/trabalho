"""
URL configuration for sistema_admin project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs de autenticação
    path('accounts/', include('django.contrib.auth.urls')),
    
    # App principal - PDF Extractor (tela inicial)
    path('', include('apps.pdf_extractor.urls')),
    
    # URLs Web - Pessoas
    path('fornecedores/', include('apps.fornecedores.urls_web')),
    path('clientes/', include('apps.clientes.urls_web')),
    path('faturados/', include('apps.faturados.urls_web')),
    
    # URLs Web - Contas
    path('contas-pagar/', include('apps.contas_pagar.urls_web')),
    path('contas-receber/', include('apps.contas_receber.urls_web')),
    
    # URLs Web - Classificações
    path('tipos-despesa/', include('apps.tipos_despesa.urls_web')),
    path('tipos-receita/', include('apps.tipos_receita.urls_web')),
    
    # URLs Web - Ferramentas
    path('pdf-processor/', include('apps.pdf_processor.urls_web')),
    path('rag/', include('apps.rag.urls')),
]

# Servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
