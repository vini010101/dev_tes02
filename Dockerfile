# Usar uma imagem base com Python
FROM python:3.12.6

# Setar o diretório de trabalho para a aplicação
WORKDIR /app

# Copiar os arquivos de requisitos para o container
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação para o container
COPY . .

# Instalar dependências extras que não estão no requirements.txt
RUN pip install jinja2 bcrypt

# Adicionando o wait-for-it.sh ao contêiner
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Expôr a porta em que o FastAPI irá rodar
EXPOSE 8000

# Comando para iniciar o servidor FastAPI, com o script wait-for-it.sh para aguardar o MySQL
ENTRYPOINT ["./wait-for-it.sh", "mysql:3306", "--", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Adicionando o wait-for-it.sh ao contêiner
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh
RUN pip install cryptography

