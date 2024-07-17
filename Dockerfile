# Use uma imagem base com Python 3.9
FROM python:3.9-slim

# Instale as dependências do sistema em etapas separadas
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    python3-virtualenv \
    libacl1-dev \
    libacl1 \
    libssl-dev \
    liblz4-dev \
    libzstd-dev \
    libxxhash-dev \
    build-essential \
    pkg-config \
    python3-pkgconfig

RUN apt-get install -y \
    libfuse-dev \
    fuse

RUN apt-get install -y \
    libfuse3-dev \
    fuse3

RUN apt-get install -y \
    borgbackup \
    git

# Limpe o cache do apt-get
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Crie e ative um ambiente virtual Python
RUN python3 -m virtualenv /env
ENV PATH="/env/bin:$PATH"

# Instale as dependências Python
RUN pip install --upgrade pip
RUN pip install python-dotenv borgapi fastapi
# Use build arguments para fornecer o token de acesso pessoal
ARG GITHUB_TOKEN

# Clone o repositório usando o token de acesso pessoal
RUN git clone https://${GITHUB_TOKEN}@github.com/EosBot/6sidesbackuptool.git /app

# Defina o diretório de trabalho
WORKDIR /app

# Copie todos os arquivos do diretório atual para /app
#COPY . /app

# Exponha a porta da aplicação FastAPI
EXPOSE 8000

# Comando para iniciar a aplicação FastAPI
CMD ["fastapi", "run","main.py"]