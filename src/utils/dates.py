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

def dia_da_semana(data1, data2): #Etapa 3 - descobrir dia da semana
    dia_semana1 = data1.weekday()
    print(data1, " : ", dia_semana1)
    dia_semana2 = data2.weekday()
    print(data2, " : ", dia_semana2)
    return data1.weekday(), data2.weekday()


def controle_data(data1, data2): #Etapa 4, 5 e 6- integrar feriados
    feriados = holidays.BR(state='DF', years=[data1.year, data2.year])
    while data1.weekday() >= 5 or data1 in feriados:
        print("Data: ", data1, "não é valida, verificando próximo dia util...")
        data1 += timedelta(days=1)
    while data2.weekday() >= 5 or data2 in feriados:
        print("Data: ", data2, "não é valida, verificando próximo dia util...")
        data2 += timedelta(days=1)
    return data1, data2

mes, ano = mes_ano_atual()
data1, data2 = datas_mensais(mes, ano)

print("Mês e Ano")
print(mes_ano_atual())
print("Datas: ")
print(datas_mensais(mes, ano))
print("Dia da Semana: ")
print( dia_da_semana(data1, data2))
print("Verificação de data")
data1, data2 = controle_data(data1, data2)
print("Datas válidas: \n", data1, "\n", data2)