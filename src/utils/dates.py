from datetime import datetime, timedelta
from collections import deque

# As datas de envio de relatório funcionam como uma FILA (FIFO)
# A primeira data a entrar é a primeira a sair quando chegar seu dia de processamento
# Quando uma data sai, uma nova é adicionada no final da fila
# Mantém sempre 6 datas futuras na fila para agendamento

# Data inicial dos envios quinzenais
DATA_INICIAL = datetime(2026, 2, 24)

# Fila global de datas quinzenais
fila_datas = deque()

def inicializar_fila(data_inicial_datetime, quantidade_datas=6):
    """
    Inicializa a fila com datas quinzenais
    
    Args:
        data_inicial_datetime: datetime object com a primeira data
        quantidade_datas: quantas datas manter na fila (padrão: 6)
    
    Returns:
        deque com as datas quinzenais
    """
    global fila_datas
    fila_datas.clear()
    
    for i in range(quantidade_datas):
        nova_data = data_inicial_datetime + timedelta(days=15 * i)
        fila_datas.append(nova_data.strftime("%d-%m-%Y")) 
        #'append' adiciona no final da fila (FIFO)
        #'.strftime("%Y-%m-%d")' para manter apenas a parte da data, sem hora
    return fila_datas

def obter_proxima_data():
    """Retorna a próxima data quinzenal (primeira da fila)"""
    if fila_datas:
        return fila_datas[0]
    return None

def processar_data():
    """
    Remove a data da frente da fila e adiciona uma nova no final
    (simula o processamento de um envio)
    """
    if fila_datas:
        data_removida = fila_datas.popleft()  # Remove da frente (FIFO)
        
        # Adiciona a próxima data quinzenal no final da fila
        ultima_data = fila_datas[-1] if fila_datas else data_removida
        proxima_data = ultima_data + timedelta(days=15)
        fila_datas.append(proxima_data)
        
        return data_removida
    return None

def eh_dia_de_envio():
    """Verifica se hoje é o dia de enviar o relatório"""
    hoje = datetime.now().date()
    proxima_data = obter_proxima_data()
    
    if proxima_data and hoje == proxima_data:
        return True
    return False

def listar_proximas_datas():
    """Retorna todas as datas presentes na fila"""
    return list(fila_datas)

# Inicializar a fila
inicializar_fila(DATA_INICIAL, quantidade_datas=6)

# Testes
print("Fila inicial:", listar_proximas_datas())
print("Próxima data de envio:", obter_proxima_data())
print("É dia de envio?", eh_dia_de_envio())