from docx import Document #Usada para manipular documentos Word
import pandas as pd #Usado para manipular e acessar dados em formato de tabela (CSV)
import os #Biblioteca padrão para interação com o Sistema Operacional

#Constantes são escritas em letras maiúsculas para indicar que seus valores não devem ser alterados durante a execução do programa
SECOES_IGNORADAS = ['DATA', 'RELATÓRIO/DRCI'] #Lista de seções que serão ignoradas durante a extração de conteúdo do documento
ESTILO_TITULO = 'Heading 1' #Definição do estilo de título a ser utilizado para identificar as seções 'titúlo' no documento
ESTILO_SUBTITULO = 'subtitulo' #Definição do estilo de subtítulo a ser utilizado para identificar as seções 'subtitulos' no documento
MINIMO_CARACTERES = 90

def carregar_csv(caminho_csv):
    if caminho_csv is None: #Verifica se o caminho do arquivo CSV foi fornecido
        print(f"Erro: O caminho do arquivo CSV não foi fornecido.")
        exit(1) #Encerra o programa com código de status 1 (indica erro)

    if not os.path.exists(caminho_csv): #Verifica se o arquivo existe no caminho especificado
        print("Erro: O arquivo CSV não foi encontrado no caminho especificado.")
        exit(1) #Encerra o programa com código de status 1 (indica erro)

    df = pd.read_csv(caminho_csv) #Lê o arquivo CSV e armazena seu conteúdo em um DataFrame do pandas para facilitar a manipulação dos dados
    return df #Retorna o DataFrame contendo os dados do arquivo CSV para uso posterior no programa

def carregar_documento(caminho_docx):
    if caminho_docx is None: #Verifica se o caminho do arquivo não esta vazio
        print(f"Erro: O caminho do arquivo DOCX não foi fornecido.")
        exit(1) #Encerra o programa com código de status 1 (indica erro)
    
    if not os.path.exists(caminho_docx): #Verifica se o arquivo existe no caminho especificado
        print("Erro: O arquivo não foi encontrado no caminho especificado")
        exit(1) #Encerra o programa com código de status 1 (indica erro)
    
    documento = Document(caminho_docx)
    return documento

def verificar_preenchimento(documento):
    dicionario = {} #
    paragrafos = documento.paragraphs #Recebe a lista de paragrafos do documento
    for i, paragrafo in enumerate(paragrafos): #Lista por número cada paragrafo
        if paragrafo.style.name == ESTILO_TITULO: #Se o nome do estilo do paragrafo atual for = Estilo_Titulo
            if paragrafo.text in SECOES_IGNORADAS: #Se o texto do paragrafo atual estiver em SECOES_IGNORADAS
                #continue 
                if i + 1 < len(paragrafos): #Se i + 1 for menor que o número de paragrafos
                    proximo_paragrafo = paragrafos[i + 1] #Proximo_paragrafo recebe o numero de i + 1

                    if proximo_paragrafo.style.name == ESTILO_TITULO: #Se o nome do estilo do proximo paragrafo for = ESTILO_TITULO
                        texto_titulo = paragrafo.texto
                        sigla = texto_titulo.split("(")[1].replace(")", "").strip() #.split() separa a string a partir do caractere, .replace() substitui um caractere pela string vazia, .strip() retira espeços vazios
                        texto_conteudo = ""
                        for j in range (i+1, len(paragrafos)): 
                            if paragrafos[j].style.name == ESTILO_TITULO: 
                                break
                            texto_conteudo += paragrafos[j].text #'+=' == incrementa
                        dicionario[sigla] = len(texto_conteudo) >= MINIMO_CARACTERES
                        return dicionario

                    elif proximo_paragrafo.style.name == ESTILO_SUBTITULO: #Se o nome do estilo do proximo paragrafo for = ESTILO_SUBTITULO
                        print("ola")

if __name__ = "__main__":
    doc = carregar_documento()