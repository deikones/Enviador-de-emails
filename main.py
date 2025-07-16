

"""
================================================================================
        Sistema de Automação de Envio de E-mails
================================================================================

Descrição:
Este script foi criado para automatizar o envio de e-mails a partir de uma lista
de participantes em um arquivo CSV. Cada e-mail é personalizado com o nome do
destinatário e contém um anexo em PDF.

O sistema inclui uma funcionalidade para alternar entre múltiplas contas de e-mail
do Gmail para contornar os limites de envio diário, tornando-o ideal para
eventos e outras necessidades de envio em massa.

Autoria e Uso:
Este código foi desenvolvido por Artur Galiza Magalhães. Ele é de código aberto
e pode ser livremente utilizado e modificado.

"""

# --- 1: IMPORTAÇÕES ---
import smtplib
import ssl
import time
import os
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# ==============================================================================
# =================== ÁREA DE CONFIGURAÇÃO DO USUÁRIO ==========================
# ==============================================================================

# 1. CONTAS DE E-MAIL (Adicione quantas contas precisar)
#    Para cada conta, você precisa de um e-mail e uma "Senha de App" de 16
#    dígitos gerada no Google.
CONTAS = [
    {
        "email": "seu_email_1@gmail.com",
        "senha_app": "xxxx xxxx xxxx xxxx"
    },
    {
        "email": "seu_email_2@gmail.com",
        "senha_app": "yyyy yyyy yyyy yyyy"
    }
]

# 2. ARQUIVOS
#    Coloque os nomes dos seus arquivos CSV e PDF aqui.
ARQUIVO_CSV_PARTICIPANTES = "participantes.csv"
ARQUIVO_PDF_ANEXO = "prova.pdf"

# 3. CONTEÚDO DO E-MAIL
ASSUNTO_EMAIL = "Seu Assunto"
CORPO_EMAIL_HTML = """
<html><body>
    <p>Prezados(as) participantes,</p>
    <p>O Desafio CNQ 2025 está oficialmente liberado!</p>
    <p>Em anexo, vocês encontrarão o PDF com a prova. As respostas devem ser enviadas até o dia 15/07 por meio do formulário a seguir:</p>
    <p><a href="https://SEU_LINK_AQUI"><b>CLIQUE AQUI PARA ENVIAR AS RESPOSTAS</b></a></p>
    <p>Boa sorte!</p><br><p>Atenciosamente,<br>Equipe CNQ</p>
</body></html>
"""

# 4. CONFIGURAÇÕES DE ENVIO
#    Limite de e-mails a serem enviados por cada conta antes de trocar.
#    450 é um valor seguro para o limite de ~500 do Gmail.
LIMITE_POR_CONTA = 450

#    Pausa em segundos entre cada e-mail para evitar bloqueio por spam.
PAUSA_ENTRE_EMAILS = 2


# ================== FIM DA CONFIGURAÇÃO ==============


def ler_e_limpar_planilha(caminho_arquivo):
    """Lê e prepara a planilha de participantes."""
    print(f"\nLendo o arquivo de participantes: '{caminho_arquivo}'...")
    if not os.path.exists(caminho_arquivo):
        print(f"🚨 ERRO CRÍTICO: Arquivo '{caminho_arquivo}' não encontrado.")
        return None

    try:
        df = pd.read_csv(caminho_arquivo)
        print(f"✅ Arquivo encontrado com {len(df)} participante(s).")

        # Garante que as colunas 'NOME' e 'EMAIL' existam.
        if 'NOME' not in df.columns or 'EMAIL' not in df.columns:
            print("🚨 ERRO: A planilha CSV deve conter as colunas 'NOME' e 'EMAIL'.")
            return None

        # Limpa espaços em branco extras dos dados para evitar erros.
        df['NOME'] = df['NOME'].astype(str).str.strip()
        df['EMAIL'] = df['EMAIL'].astype(str).str.strip()
        print("✅ Dados de nome e e-mail limpos.")
        
        return df.to_dict('records')

    except Exception as e:
        print(f"🚨 ERRO inesperado ao ler o arquivo CSV: {e}")
        return None


def enviar_emails(lista_alunos):
    """Processo de envio dos e-mails."""
    if not lista_alunos:
        print("Nenhum aluno na lista para enviar. Encerrando.")
        return

    indice_conta_atual = 0
    enviados_pela_conta_atual = 0
    servidor = None

    try:
        # Conecta com a primeira conta
        conta_atual = CONTAS[indice_conta_atual]
        print(f"\n--- Conectando com a conta: {conta_atual['email']} ---")
        
        # Bloco de conexão segura com o servidor do Gmail.
        contexto_ssl = ssl.create_default_context()
        servidor = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto_ssl)
        servidor.login(conta_atual['email'], conta_atual['senha_app'])
        print(f"✅ Login bem-sucedido.")

        for i, student in enumerate(lista_alunos):
            # Lógica para trocar de conta quando o limite é atingido
            if enviados_pela_conta_atual >= LIMITE_POR_CONTA and (indice_conta_atual + 1) < len(CONTAS):
                servidor.quit()
                indice_conta_atual += 1
                enviados_pela_conta_atual = 0
                conta_atual = CONTAS[indice_conta_atual]

                print(f"\n--- Limite atingido. Trocando para a conta: {conta_atual['email']} ---")
                servidor = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto_ssl)
                servidor.login(conta_atual['email'], conta_atual['senha_app'])
                print("✅ Login na nova conta bem-sucedido.")

            recipient_name = student.get('NOME', 'Participante')
            recipient_email = student.get('EMAIL')

            # Pula a linha se o e-mail for inválido
            if not isinstance(recipient_email, str) or '@' not in recipient_email:
                print(f"\n({i+1}/{len(lista_alunos)}) ⚠️ Pulando e-mail inválido: '{recipient_email}'")
                continue

            print(f"\n({i+1}/{len(lista_alunos)}) Preparando para: {recipient_name} ({recipient_email})")
            
            msg = MIMEMultipart()
            msg['From'] = f"Equipe CNQ <{conta_atual['email']}>"
            msg['To'] = recipient_email
            msg['Subject'] = ASSUNTO_EMAIL
            msg.attach(MIMEText(CORPO_EMAIL_HTML, 'html'))

            # Anexa o PDF
            try:
                with open(ARQUIVO_PDF_ANEXO, "rb") as f:
                    attach = MIMEApplication(f.read(), _subtype="pdf")
                attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(ARQUIVO_PDF_ANEXO))
                msg.attach(attach)
            except FileNotFoundError:
                print(f"🚨 ERRO: O arquivo PDF '{ARQUIVO_PDF_ANEXO}' não foi encontrado.")
                continue

            servidor.sendmail(conta_atual['email'], recipient_email, msg.as_string())
            print(f"✅ E-mail enviado com sucesso.")
            enviados_pela_conta_atual += 1
            
            time.sleep(PAUSA_ENTRE_EMAILS)

    except smtplib.SMTPAuthenticationError:
        print("\n🚨 ERRO DE AUTENTICAÇÃO: Verifique se o e-mail e a Senha de App estão corretos na área de configuração.")
    except Exception as e:
        print(f"\n🚨 UM ERRO CRÍTICO OCORREU: {e}")
    finally:
        if servidor:
            servidor.quit()
        print("\n--- Processo de envio finalizado. ---")


def main():
    """Função principal que orquestra a execução do script."""
    print("Iniciando Sistema de Automação de E-mails CNQ")
    lista_de_alunos = ler_e_limpar_planilha(ARQUIVO_CSV_PARTICIPANTES)
    enviar_emails(lista_de_alunos)


if __name__ == "__main__":
    main()

