from docx import Document #Usada para manipular documentos Word
import pandas as pd #Usado para manipular e acessar dados em formato de tabela (CSV)
import os #Biblioteca padrão para interação com o Sistema Operacional

doc = Document(r"C:\Users\sharyssa.silva\OneDrive - MINISTERIO DA JUSTIÇA\Documentos\00_EM_PREENCHIMENTO\00 - 2026 Relatório Quinzenal DRCI - Modelo Editavel.docx") 
#O 'R' antes da string indica uma 'Raw String' (string bruta), que trata a barra invertida como um caractere
#Isso possibilita a interpretação da string dessa forma, como um caminho de arquivo

SECOES_IGNORADAS = ["DATA", "RELATÓRIO/DRCI N° __/2026"] #Sessôes que serão ignoradas, preenchidas antes do documento ser processado
LIMIAR_PREENCHIMENTO = 20 #Quantidade de caracteres mínimos para considerar um campo como preenchido, pode ser alterado

def extrair_secao(doc, sigla): 
    #Extrai o texto de uma seção e a sigla é usada para identificar a seção específica a ser extraída do documento

    paragrafos = doc.paragraphs #Lista de parágrafos do documento, cada paragrafo é um objeto que contém o texto e o estilo - Ex: 'Heading 1' 
    resultado = {} #Dicionário para armazenar a chave = nome do campo e valor = conteúdo do campo
    i = 0 

    while i < len(paragrafos): #len é usada para medir o tamanho e/ou quantidade de itens dentro de um objeto
        paragrafo_atual = paragrafos[i]

        if paragrafo_atual.style.name == "Heading 1": 
            
            if sigla in paragrafo_atual.text: 
                i += 1 
                proximo = paragrafos[i] if i <len(paragrafos) else None

                if proximo and proximo.style.name == "subtitulos":

                    while i < len(paragrafos) and paragrafos[i].style.name != "Heading 1":

                        if paragrafos[i].style.name == "subtitulos":
                            nome_campo = paragrafos[i].text.strip()
                            conteudo = []
                            i += 1 

                            while i < len(paragrafos) and paragrafos[i].style.name not in ["Heading 1", "subtitulos"]:
                                conteudo.append(paragrafos[i].text.strip())
                                i += 1

                            resultado[nome_campo] = " ".join(conteudo)
                        else:
                            i +=1

                else:
                    conteudo = []

                    while i <len(paragrafos) and paragrafos[i].style.name != "Heading 1":
                        conteudo.append(paragrafos[i].text.strip())
                        i += 1
                        
                    resultado[paragrafo_atual.text.strip()] = " ".join(conteudo)
                    
                return resultado
        i += 1
    return resultado

def secao_completa(campos):
    if not campos: 
        return False
    
    for campo, conteudo in campos.itens(): 
        
        if len(conteudo) <LIMIAR_PREENCHIMENTO:
            
            return False
    return True

def processar_watcher():
    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    dotenv_path = os.path.join(script_dir, '../../config/.env')
     

    from dotenv import load_dotenv
    load_dotenv(dotenv_path)
    

    caminho_csv = os.getenv("PATH_DATA")
    data_path = os.path.abspath(os.path.join(script_dir, '../../' + caminho_csv))

    df = pd.read_csv(data_path)

    atualizad = False

    for index, row in df.interrows():
        nome = row['nome']
        sigla = row['sigla']
        status = row['status']
        caminho_doc = row['link_documento']

        if status == 'Aprovado':
            print(f"Pulando {nome} - já aprovado")
            continue

        if not os.path.exists(caminho_doc):
            print(f"Documento não encontrado para {nome}: {caminho_doc}")
            continue
        print(f"\nAnalisando {nome} ({sigla})...")

        doc = Document(caminho_doc)
        campos = extrair_secao(doc, sigla)

        if not campos:
            print(f"Seção {sigla} não encontrada no documento")
            continue

        if secao_completa(campos):
            novo_status = 'A Validar'

        elif any(len(c) >= LIMIAR_PREENCHIMENTO for c in campos.values()):
            novo_status = 'Em Preenchimento'
        else:
            novo_status = 'Pendente'

        if novo_status != status:
            print(f"{nome}: {status} -> {novo_status}")
            df.at[index, 'status'] = novo_status
            atualizado = True
        else:
            print(f"{nome}: sem alterações ({status})")

    if atualizado:
        df.to_csv(data_path,indez = False)
        print("\nCSV atualizado com sucesso!")
    else:
        print("\n Nenhuma atualização detectada.")

if __name__ == "__main__":
    processar_watcher()