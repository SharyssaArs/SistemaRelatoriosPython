from datetime import datetime
from docx import Document
import pandas as pd
import os
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '../../config/.env')
load_dotenv(dotenv_path)

# Constantes
SECOES_IGNORADAS = ['DATA', 'RELATÓRIO/DRCI']
TITULOS_SEM_SUBTITULOS = ['REUNIÕES TRANSVERSAIS – DRCI']
ESTILO_TITULO = 'Head1'
ESTILO_SUBTITULO = 'Head2'
MINIMO_CARACTERES = 90

def carregar_csv(caminho_csv):
    if caminho_csv is None:
        print("Erro: O caminho do arquivo CSV não foi fornecido.")
        exit(1)
    if not os.path.exists(caminho_csv):
        print("Erro: O arquivo CSV não foi encontrado no caminho especificado.")
        exit(1)
    df = pd.read_csv(caminho_csv)
    return df

def carregar_documento(caminho_docx):
    if caminho_docx is None:
        print("Erro: O caminho do arquivo DOCX não foi fornecido.")
        exit(1)
    if not os.path.exists(caminho_docx):
        print("Erro: O arquivo não foi encontrado no caminho especificado.")
        exit(1)
    documento = Document(caminho_docx)
    return documento

def verificar_preenchimento(documento):
    dicionario = {}
    paragrafos = documento.paragraphs

    for i, paragrafo in enumerate(paragrafos):
        if paragrafo.style.name == ESTILO_TITULO:

            # Pula seções ignoradas
            if paragrafo.text in SECOES_IGNORADAS:
                continue

            # Extrai a sigla do título
            texto_titulo = paragrafo.text
            if "(" in texto_titulo:
                sigla = texto_titulo.split("(")[1].replace(")", "").strip()
            else:
                sigla = texto_titulo.strip()

            # Caso 1 — título sem subtítulos, preenchido diretamente
            if any(titulo in texto_titulo for titulo in TITULOS_SEM_SUBTITULOS):
                texto_conteudo = ""
                for j in range(i + 1, len(paragrafos)):
                    if paragrafos[j].style.name == ESTILO_TITULO:
                        break
                    texto_conteudo += paragrafos[j].text
                dicionario[sigla] = len(texto_conteudo) >= MINIMO_CARACTERES

            # Caso 2 — título com subtítulos
            else:
                total_subtitulos = 0
                subtitulos_preenchidos = 0
                for j in range(i + 1, len(paragrafos)):
                    if paragrafos[j].style.name == ESTILO_TITULO:
                        break
                    if paragrafos[j].style.name == ESTILO_SUBTITULO:
                        total_subtitulos += 1
                        texto_subtitulo = ""
                        for k in range(j + 1, len(paragrafos)):
                            if paragrafos[k].style.name == ESTILO_TITULO or paragrafos[k].style.name == ESTILO_SUBTITULO:
                                break
                            texto_subtitulo += paragrafos[k].text
                        if len(texto_subtitulo) >= MINIMO_CARACTERES:
                            subtitulos_preenchidos += 1
                dicionario[sigla] = subtitulos_preenchidos == total_subtitulos
    return dicionario

def atualizar_csv(df, resultados, caminho_csv):
    print(f"Caminho CSV: {caminho_csv}")
    print(f"Resultados: {resultados}")
    print(f"Siglas no CSV: {df['sigla'].tolist()}")    
    for index, row in df.iterrows():
        if row['sigla'] in resultados:
            if resultados[row['sigla']] == True:
                df.at[index, 'status'] = 'A Validar'
            else:
                df.at[index, 'status'] = 'Pendente'
            df.at[index, 'ultima_atualizacao'] = datetime.now().strftime("%d/%m/%Y %H:%M")
    df.to_csv(caminho_csv, index=False)

def executar_watcher():
    caminho_docx = r"C:\Users\sharyssa.silva\OneDrive - MINISTERIO DA JUSTIÇA\Documentos\00_EM_PREENCHIMENTO\01 - 2026 Relatório Quinzenal DRCI.docx"
    caminho_csv = os.getenv('PATH_DATA')
    df = carregar_csv(caminho_csv)
    doc = carregar_documento(caminho_docx)
    resultados = verificar_preenchimento(doc)
    atualizar_csv(df, resultados, caminho_csv)

if __name__ == "__main__":
    executar_watcher()