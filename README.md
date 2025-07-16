Sistema de Automação de Envio de E-mails em Lote
Este projeto foi desenvolvido para automatizar o envio de um grande volume de e-mails personalizados, cada um com um anexo em PDF, a partir de uma lista de contatos em um arquivo CSV.

🎯 Propósito
O objetivo deste projeto foi criar uma solução automatizada para enviar 800 e-mails personalizados para os participantes da Olimpíada Nacional de Química (CNQ). A meta era garantir que cada aluno recebesse o arquivo da prova em PDF de forma rápida e confiável, algo inviável de se fazer manualmente.

챌 Desafios Técnicos
O principal obstáculo técnico foi contornar as barreiras de autenticação e os limites de envio do Gmail. As tentativas iniciais de ler a lista de participantes diretamente da API do Google Sheets resultaram em constantes falhas de autorização (OAuth 2.0). Além disso, o limite de envios diário do Gmail impedia que todos os e-mails fossem despachados por uma única conta.

💡 Solução e Tecnologias
Para resolver esses problemas, desenvolvi um script em Python. A abordagem final foi migrar de uma solução online para um processamento local, utilizando a biblioteca pandas para ler e limpar os dados dos participantes a partir de um arquivo CSV, o que se mostrou muito mais estável. Para o envio, usei a biblioteca smtplib, implementando uma lógica inteligente de contador para trocar de conta de e-mail automaticamente antes que o limite do provedor fosse atingido.

Tecnologias Utilizadas:

Python 3

Pandas: Para manipulação e limpeza de dados do arquivo CSV.

Smtplib & SSL: Para a comunicação segura com o servidor de e-mail do Gmail.

Email (MIMEMultipart): Para a construção da estrutura do e-mail com anexos.

🚀 Como Usar
Para executar este projeto, siga os passos abaixo:

1. Preparação:

Clone este repositório: git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git

Navegue até a pasta do projeto: cd NOME_DO_REPOSITORIO

2. Instalação de Dependências:

Crie um ambiente virtual (recomendado): python3 -m venv env e source env/bin/activate

Instale as bibliotecas necessárias: pip install -r requirements.txt

3. Configuração:

Renomeie o arquivo participantes_exemplo.csv para o nome do seu arquivo de contatos ou edite o script para apontar para o seu arquivo. Ele deve conter as colunas NOME e EMAIL.

Abra o arquivo main.py e edite a ÁREA DE CONFIGURAÇÃO DO USUÁRIO no topo, inserindo suas contas de e-mail, senhas de app e o conteúdo do e-mail.

4. Execução:

Execute o script a partir do seu terminal: python3 main.py

🎓 Aprendizados
Este projeto foi um exercício prático profundo em resolução de problemas. O maior aprendizado foi na depuração iterativa e no design de uma solução que não apenas executa uma tarefa, mas que também antecipa e gerencia seus próprios pontos de falha, como os limites de API e a inconsistência de dados de entrada.

Este projeto foi desenvolvido por Artur Galiza Magalhães.
