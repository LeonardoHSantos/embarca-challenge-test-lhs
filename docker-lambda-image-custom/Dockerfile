# Defina os argumentos para a imagem:
# FUNCTION_DIR - Diretório onde o código da função Lambda será armazenado.
# RUNTIME_VERSION - Versão do Python a ser usada.
# DISTRO_VERSION - Versão do Alpine Linux (distribuição leve) a ser usada.
ARG FUNCTION_DIR="/home/app/"
ARG RUNTIME_VERSION="3.9"
ARG DISTRO_VERSION="3.12"

# Use a imagem base do Python, com Alpine Linux como base para ser leve e otimizada.
# Python e Alpine são combinados para oferecer uma imagem pequena com Python instalado.
FROM python:${RUNTIME_VERSION}-alpine${DISTRO_VERSION} AS python-alpine

# Instala pacotes essenciais no ambiente Alpine:
# libstdc++ - Biblioteca padrão do C++.
# libcurl - Biblioteca usada para fazer requisições HTTP.
RUN apk add --no-cache \
    libstdc++ \
    libcurl

# Estágio de construção da imagem.
# Aqui, a imagem é preparada com ferramentas de compilação necessárias.
FROM python-alpine AS build-image

# Instala ferramentas de compilação e pacotes adicionais que serão necessários para compilar ou rodar bibliotecas nativas.
# build-base - Conjunto de ferramentas de compilação como gcc, g++.
# libtool, autoconf, automake - Utilitários para configurar e construir software.
# libexecinfo-dev - Ferramenta para depuração e coleta de stack trace.
# make, cmake - Ferramentas de automação de build.
RUN apk add --no-cache \
    build-base \
    libtool \
    autoconf \
    automake \
    libexecinfo-dev \
    make \
    cmake

# Cria o diretório onde o código da função Lambda ficará armazenado.
# Isso é útil para organizar o código da aplicação.
ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}

# Copia o código-fonte da função Lambda para o diretório criado acima.
# Neste caso, está copiando o conteúdo do diretório 'app' para FUNCTION_DIR.
COPY app/* ${FUNCTION_DIR}

# Instala o Runtime Interface Client (RIC) da AWS Lambda e outras dependências necessárias para rodar a aplicação.
# O RIC permite que a função Lambda interaja com a AWS em um ambiente local.
# `--target ${FUNCTION_DIR}` indica que as dependências serão instaladas diretamente no diretório da função.

# numpy \                 # Biblioteca para computação numérica.
# PyMySQL \               # Cliente MySQL para Python.
# python-dotenv \         # Gerenciador de variáveis de ambiente a partir de arquivos .env.
# boto3 \                 # SDK da AWS para Python.
# botocore \              # Biblioteca de baixo nível para interagir com serviços AWS.
# awslambdaric \          # AWS Lambda Runtime Interface Client (RIC).
# certifi \               # Certificados SSL.
# charset-normalizer \    # Biblioteca para codificação de texto.
# idna \                  # Suporte para nomes de domínio internacionalizados.
# jmespath \              # Ferramenta para consulta de JSON.
# python-dateutil \       # Biblioteca para manipulação avançada de datas.
# pytz \                  # Suporte a fuso horários.
# requests \              # Biblioteca para requisições HTTP.
# s3transfer \            # Ferramenta para transferência de arquivos com S3.
# six \                   # Biblioteca para compatibilidade entre Python 2 e 3.
# tzdata \                # Banco de dados de fuso horários.
# urllib3 \               # Biblioteca para conexões HTTP.
# --target ${FUNCTION_DIR}  # Instala as dependências diretamente no diretório da função.

RUN python${RUNTIME_VERSION} -m pip install \
    numpy \
    PyMySQL \
    python-dotenv \
    boto3 \
    botocore \
    awslambdaric \
    certifi \
    charset-normalizer \
    idna \
    jmespath \
    python-dateutil \
    pytz \
    requests \
    s3transfer \
    six \
    tzdata \
    urllib3 \
    --target ${FUNCTION_DIR} # Instala as dependências diretamente no diretório da função.

# Agora vamos criar a imagem final que será usada para executar a função Lambda.

# Começa novamente com a imagem base python-alpine para ter uma imagem limpa.
FROM python-alpine

# Define o diretório de trabalho da função Lambda, que foi criado e preparado no estágio anterior.
ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}

# Copia todos os arquivos do estágio de build para o estágio final, incluindo o código e as dependências da função Lambda.
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Baixa o AWS Lambda Runtime Interface Emulator (RIE), que é usado para simular o ambiente AWS Lambda em execução local.
# Isso permite testar a função Lambda localmente de maneira muito próxima à execução real na AWS.
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/download/v1.22/aws-lambda-rie /usr/bin/aws-lambda-rie

# Copia o script de entrada (entrypoint) que será usado para iniciar a função Lambda.
# O `entry.sh` será usado para configurar e iniciar o ambiente da função.
COPY entry.sh /

# Define permissões para os binários `aws-lambda-rie` e `entry.sh` para garantir que possam ser executados.
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh
RUN chmod 755 /entry.sh

# Define o ponto de entrada (ENTRYPOINT) do contêiner, que é o script `entry.sh`.
# Isso garante que quando o contêiner for iniciado, ele irá configurar o ambiente Lambda antes de executar a função.
ENTRYPOINT [ "/entry.sh" ]

# Define o comando padrão (CMD) que será executado depois que o contêiner estiver pronto.
# Aqui, estamos dizendo para o contêiner executar a função `lambda_handler` dentro do arquivo `lambda_function.py`.
CMD [ "lambda_function.lambda_handler" ]