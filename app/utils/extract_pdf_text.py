#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extrair texto do PDF do projeto administrativo
"""

try:
    import PyPDF2
    PDF_LIBRARY = "PyPDF2"
except ImportError:
    try:
        import pdfplumber
        PDF_LIBRARY = "pdfplumber"
    except ImportError:
        PDF_LIBRARY = None

def extract_text_from_pdf(pdf_path):
    """
    Extrai texto de um arquivo PDF usando a biblioteca disponível
    """
    if PDF_LIBRARY is None:
        print("Erro: Nenhuma biblioteca de PDF encontrada.")
        print("Instale uma das seguintes bibliotecas:")
        print("pip install PyPDF2")
        print("ou")
        print("pip install pdfplumber")
        return None
    
    try:
        if PDF_LIBRARY == "PyPDF2":
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += f"\n--- PÁGINA {page_num + 1} ---\n"
                    text += page.extract_text()
                return text
        
        elif PDF_LIBRARY == "pdfplumber":
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page_num, page in enumerate(pdf.pages):
                    text += f"\n--- PÁGINA {page_num + 1} ---\n"
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                return text
                
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        return None

def main():
    pdf_file = "PROJETO ADMINISTRATIVO - N2 - Etapa 1.pdf"
    
    print("Extraindo texto do PDF...")
    text = extract_text_from_pdf(pdf_file)
    
    if text:
        # Salva o texto extraído em um arquivo
        with open("texto_extraido.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Texto extraído salvo em 'texto_extraido.txt'")
        print("\nPrimeiras 1000 caracteres do texto:")
        print(text[:1000])
    else:
        print("Não foi possível extrair o texto do PDF")

if __name__ == "__main__":
    main()

