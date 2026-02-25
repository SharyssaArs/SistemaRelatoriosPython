from dotenv import load_dotenv
import pandas as pd
import os
from src.utils.dates import inicializar_fila, eh_dia_de_envio, processar_data, obter_proxima_data, listar_proximas_datas
from src.utils.email import enviar_email

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

# Lê o arquivo
df = pd.read_csv(data_path)

#Visualiza as primeiras linhas
print(df.head())

def processar_envio_quinzenal():
    #Se 'hoje == proxima_data', envia o email e processa a fila
    if eh_dia_de_envio():
        print(f"Hoje é dia de envio!")
        data_processada = processar_data() #Remove a data da fila e adiciona a próxima
        print(f"Relatório enviado em: {data_processada}") #Mostra a data que foi processada (removida da fila) - data do envio
        
        # Itera por cada linha do CSV
        for index, row in df.iterrows():
            nome = row['nome']
            email = row['email']
            status = row['status']
            
            # Envia apenas para os com status "Pendente"
            if status == 'Pendente':
                print(f"\nEnviando para {nome} ({email})...")
                enviar_email(
                    destinatario=email,
                    assunto="Relatório Quinzenal",
                    mensagem=f"Olá {nome},\n\nSegue em anexo seu relatório.\n\nAtt"
                )
            else:
                print(f"Pulando {nome} - Status: {status}")
        
        print(f"\nPróximo envio: {obter_proxima_data()}")
        print("\n✓ Todos os emails foram enviados com sucesso!")
        return True
    else:
        proxima = obter_proxima_data()
        print(f"Hoje não é dia de envio.")
        print(f"Próximo envio programado para: {proxima}")
        return False

# Executa o processamento de envio
if __name__ == "__main__":
    processar_envio_quinzenal()