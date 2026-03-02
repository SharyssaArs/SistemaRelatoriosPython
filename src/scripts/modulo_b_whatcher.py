from docx import Document
import pandas as pd
import os

doc = Document(r"C:\Users\sharyssa.silva\OneDrive - MINISTERIO DA JUSTIÇA\Documentos\00_EM_PREENCHIMENTO\00 - 2026 Relatório Quinzenal DRCI - Modelo Editavel.docx") 
#O 'R' antes da string indica que é uma string bruta, útil para caminhos de arquivos no Windows

SECOES_IGNORADAS = ["DATA", "RELATÓRIO/DRCI N° __/2026"]
LIMIAR_PREENCHIMENTO = 20

def extrair_secao(doc, sigla): #Extrai o texto da seção correspondente à sigla, ignorando as seções listadas em SECOES_IGNORADAS
    paragrafos = doc.paragraphs #Obtém todos os parágrafos do documento
    resultado = {} #Dicionário para armazenar o texto extraído de cada seção
    i = 0 #Índice para percorrer os parágrafos

    while i < len(paragrafos): #len(paragrafos) retorna o número total de parágrafos no documento
        paragrafo_atual = paragrafos[i]

        if paragrafo_atual.style.name == "Heading 1":
            if sigla in paragrafo_atual.text:
                i += 1
                
