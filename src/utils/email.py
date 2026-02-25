import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

#- `smtplib` = conectar ao servidor de email (agência dos Correios)
#`MIMEText` = criar corpo de texto do email
#`MIMEMultipart` = criar um email com múltiplas partes (se precisar)

def enviar_email(destinatario, assunto, mensagem):
    #Envia um email
    
    email_remetente = os.getenv("EMAIL_REMETENTE") 
    senha_email = os.getenv("SENHA_EMAIL")
    servidor_smtp = os.getenv("SERVIDOR_SMTP")
    porta_smtp = int(os.getenv('PORTA_SMTP', '587'))
    #'os.getenv' = é uma excelente prática de segurança, para evitar expor dados sensiveis n codigo principal.
    #Mudar de Gmail para Outlook, não precisa mexer no codigo, basta alterar no arquivo de config
    #'os.getenv' = pega o valor do aqruivo .env
    #Exemplo: '.env' tem 'EMAIL_REMETENTE = email.exemplo@email.com'
    # email_remetente = EMAIL_REMETENTE
    #SMTP (Simple Mail Transfer Protocol)
    #Servidor = Agencia dos Correios
    #Servidor é o endereço do computador da empresa de email (Ex: Gmail 'smtp.gmail.com', Outlook 'smtp.office265.com')
    #Porta = Guiche o servidor do email
    #Porta 587 = TLS (Transport Layer Security) - conversa criptografada

    if not all([email_remetente, senha_email, servidor_smtp]):
        print("Erro: Variáveis de ambiente para email não estão configuradas corretamente.")
        return False
    #all([...]) = verifica se TODOS tem valor
    #not all([...]) = se NÃo tem todos os valores
    #Se faltar algo, avisa e sai (return False)

    try:
        msg = MIMEMultipart()  #Cria um email vazio
        msg['From'] = email_remetente #Define o remetente do email
        msg['To'] = destinatario #Define o destinatário do email
        msg['Subject'] = assunto #Define o assunto do email
        msg.attach(MIMEText(mensagem, 'plain', 'utf-8'))  #Anexa o corpo do email (texto simples, codificação UTF-8)
        #`'plain'` = texto simples (não HTML) - `'utf-8'` = com suporte a acentos

        with smtplib.SMTP(servidor_smtp, porta_smtp) as server: #Conecta ao servidor SMTP
            server.starttls() #Inicia a comunicação segura (TLS)
            server.login(email_remetente, senha_email) #Faz login no servidor de email com o remetente e senha
            server.send_message(msg) #Envia o email criado (msg) para o destinatário
        
        print("Email enviado com sucesso!")
        return True
    
    except smtplib.SMTPAuthenticationError: #Erro de autenticação (senha ou email errados)
        print("Erro de autenticação: Verifique o email e senha.") 
        return False
    
    except smtplib.SMTPException as e: #Problemas relacionados ao SMTP (conexão, envio, etc)
        print(f"Erro ao enviar email: {e}")
        return False
    
    except Exception as e: #Qualquer outro erro inesperado
        print(f"Erro inesperado: {e}")
        return False