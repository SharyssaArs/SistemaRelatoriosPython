from datetime import datetime, timedelta, date
from collections import deque
import holidays
import locale

# As datas de envio de relatório funcionam como uma FILA (FIFO)
# A primeira data a entrar é a primeira a sair quando chegar seu dia de processamento
# Quando uma data sai, uma nova é adicionada no final da fila
# Mantém sempre 6 datas futuras na fila para agendamento

def mes_ano_atual(): #Etapa 1 - pegar mes e ano atual
    #date.toda() pega a data atual, .month extrai o mês
    hoje = date.today()
    mes = hoje.month
    data1 =

