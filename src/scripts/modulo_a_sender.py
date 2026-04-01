from dotenv import load_dotenv
import pandas as pd
import os
from src.utils.dates import (mes_ano_atual, datas_mensais, controle_data, dia_de_envio, gerar_periodo, gerar_prazo)
from src.utils.emails import enviar_email

# Carrega as configurações do arquivo que está em config/.env
# Usa o diretório do script como referência para encontrar o .env
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '../../config/.env')
load_dotenv(dotenv_path)

# Pega o caminho salvo no .env
caminho_dados = os.getenv('PATH_DATA')

# Verifica se a variável foi carregada
if caminho_dados is None:
    print(f"Erro: PATH_DATA não foi encontrado em {dotenv_path}")
    exit(1)

# Constrói o caminho absoluto do arquivo de dados
data_path = os.path.join(script_dir, '../../' + caminho_dados)
data_path = os.path.abspath(data_path)

def processar_envio_quinzenal():
    # Lê o arquivo
    df = pd.read_csv(data_path)
    #Visualiza as primeiras linhas
    print(df.head())
    #Geração das datas
    mes, ano = mes_ano_atual()
    data1, data2 = datas_mensais(mes, ano)
    data1, data2 = controle_data(data1, data2)
    primeiro_dia, ultimo_dia = gerar_periodo(data1, data2)
    prazo = gerar_prazo()

    #Se 'hoje == proxima_data', envia o email e processa a fila
    if dia_de_envio(data1, data2):        
        # Itera por cada linha do CSV
        for index, row in df.iterrows():
            nome = row['nome']
            email = row['email']
            status = row['status']
            
            # Envia apenas para os com status "Pendente"
            if status == 'Pendente':
                print(f"\nEnviando para {nome} ({email})...")
                link_documento = os.getenv('LINK_DOCUMENTO')
                enviar_email(
                    destinatario=email,
                    assunto=f"Preenchimento do Relatório Quinzenal - Período: {primeiro_dia} a {ultimo_dia}. PRAZO: {prazo}",
                    mensagem=f"Olá {nome},\n\nSeguindo a rotina do DRCI, encaminhamos o documento para preenchimento do Relatório Quinzenal, referente ao período de {primeiro_dia} a {ultimo_dia}.\n\n{link_documento}\n\nAs informações deverão ser registradas por meio do link até o dia {prazo}.\n\nAtenciosamente,\nCoordenação de Gestão Interna."
                )
            else:
                print(f"Pulando {nome} - Status: {status}")
        print("\n✓ Todos os emails foram enviados com sucesso!")
        return True
    else:
        print(f"Hoje não é dia de envio.")
        return False

# Executa o processamento de envio
if __name__ == "__main__":
    processar_envio_quinzenal()