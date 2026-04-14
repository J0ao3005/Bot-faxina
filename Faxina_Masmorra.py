import datetime
from collections import deque
import requests
import json
import urllib.parse
import os

# Lista com os 8 moradores da república
moradores = [
    'Mixirika', 'Bbzaum', 'Paldselfi', 'Jab',
    'Ze do Caroco', 'B.Guilherme', 'B.Henryke','B.Lucas'
]

# Dicionário com os cômodos e a quantidade de pessoas necessárias
tarefas = {
    "Sala + lavabo": 1,
    "Copa": 1,
    "Escada dentro de casa": 1,
    "Cozinha": 2,
    "Banheiro principal": 1,
    "Banheiro do quarto": 1,
    "Escada da entrada": 1
}


def gerar_escala():
    # Define a data exata em que essa ordem original da lista deve valer
    # Formato: Ano, Mês, Dia (Coloquei a data que a ordem atual começou a valer, por exemplo, 23/03/2026 (Sujeito a mudanças))
    data_inicio = datetime.date(2026, 4, 14) 
    hoje = datetime.date.today()
    
    # Calcula quantas semanas inteiras se passaram desde a data de início
    semanas_passadas = (hoje - data_inicio).days // 7
    
    fila_moradores = deque(moradores)
    
    # Rotaciona a fila para a DIREITA (positivo) -- (Caso queira rotacionar para a esquerda, usar um valor negativo).
    # Na primeira semana, semanas_passadas é 0, então ninguém sai do lugar.
    fila_moradores.rotate(semanas_passadas)
    
    escala = []
    
    for tarefa, qtd_vagas in tarefas.items():
        responsaveis = []
        for _ in range(qtd_vagas):
            responsaveis.append(fila_moradores.popleft())
        
        escala.append(f"{tarefa} - {' + '.join(responsaveis)}")
    
    
    return escala

def montar_mensagem(escala):
    # Calcula a data da próxima quarta-feira
    hoje = datetime.date.today()
    dias_para_quarta = (2 - hoje.weekday()) % 7
    if dias_para_quarta == 0 and hoje.weekday() != 2:
        dias_para_quarta = 7
    proxima_quarta = hoje + datetime.timedelta(days=dias_para_quarta)
    data_formatada = proxima_quarta.strftime("%d/%m")

    # Texto final (Sujeito a mudanças, principalmente a parte do emoji e formatação)
    mensagem = f"⛔ *Faxina de QUARTA-FEIRA {data_formatada}*\n\n"
    mensagem += "\n".join(escala)
    
    return mensagem

# Geração da escala

escala_atual = gerar_escala()
texto_whatsapp = montar_mensagem(escala_atual)

print(texto_whatsapp)

def enviar_whatsapp(mensagem):
    url = "https://api.callmebot.com/whatsapp.php"
    
    parametros = {
        "phone": os.environ.get("PHONE_NUMBER"), # Puxa do cofre
        "text": mensagem,
        "apikey": os.environ.get("API_KEY")      # Puxa do cofre
    }
    
    resposta = requests.get(url, params=parametros)
    
    if resposta.status_code == 200:
        print("Mensagem enviada com sucesso para a Masmorra!")
    else:
        print(f"Erro ao enviar: {resposta.text}")

# Gerando e enviando
escala_atual = gerar_escala()
texto_whatsapp = montar_mensagem(escala_atual)

# Dispara a mensagem
enviar_whatsapp(texto_whatsapp)