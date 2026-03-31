import calendar
from datetime import timedelta, date
import holidays

def mes_ano_atual(): #Etapa 1 - pegar mes e ano atual
    #date.toda() pega a data atual, .month extrai o mês
    hoje = date.today()
    return hoje.month, hoje.year

def datas_mensais(mes, ano): #Etapa 2 - montar datas
    data1 = date(ano, mes, 1)
    data2 = date(ano, mes, 16)
    return data1, data2

#dia da semana

def controle_data(data1, data2): #Etapa 4, 5 e 6- integrar feriados
    feriados = holidays.BR(state='DF', years=[data1.year, data2.year])
    while data1.weekday() >= 5 or data1 in feriados:
        data1 += timedelta(days=1)
    while data2.weekday() >= 5 or data2 in feriados:
        data2 += timedelta(days=1)
    return data1, data2

def dia_de_envio(data1, data2):
    dia_atual = date(2026, 3, 16)
    if dia_atual == data1 or dia_atual == data2:
        print("Hoje é dia de envio!")
        print("Relatório enviado em: ", dia_atual)
        return True
    else:
        return False

def gerar_periodo(data1, data2):
    dia_atual = date(2026, 3, 16)
    if data1 == dia_atual:
        primeiro_dia = data1
        ultimo_dia = data2 - timedelta(days=1)
        return primeiro_dia.strftime("%d/%m/%Y"), ultimo_dia.strftime("%d/%m/%Y")
    elif data2 == dia_atual:
        primeiro_dia = data2
        ultimo_dia = date(data2.year, data2.month, (calendar.monthrange(data2.year, data2.month)[1]))
        return primeiro_dia.strftime("%d/%m/%Y"), ultimo_dia.strftime("%d/%m/%Y")
    else:
        return None
    
def gerar_prazo():
    hoje = date.today()
    prazo = hoje + timedelta(days=5)
    feriados = holidays.BR(state='DF', years=[prazo.year, prazo.year + 1])
    while prazo.weekday() >= 5 or prazo in feriados:
        prazo += timedelta(days=1)
    return prazo.strftime("%d/%m/%Y")

