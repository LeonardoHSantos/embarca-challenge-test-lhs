# Defina as versões como argumentos
ARG FUNCTION_DIR="/home/app/"
ARG RUNTIME_VERSION="3.9"
ARG DISTRO_VERSION="3.12"

# Use Python com Alpine como imagem base
FROM python:${RUNTIME_VERSION}-alpine${DISTRO_VERSION} AS python-alpine

# Instale bibliotecas necessárias
RUN apk add --no-cache \
    libstdc++ \
    libcurl

# Estágio de construção
FROM python-alpine AS build-image

# Instale ferramentas de compilação e dependências necessárias
RUN apk add --no-cache \
    build-base \
    libtool \
    autoconf \
    automake \
    libexecinfo-dev \
    make \
    cmake

# Crie o diretório da função Lambda
ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}

# Copie o código-fonte da função Lambda
COPY app/* ${FUNCTION_DIR}


# Opcional: se nessário instalar essas bibliotecas no segundo build. Evitei de instalar direto para utilizar apenas recursos necessários da imagem Docker.
# awslambdaric boto3 botocore python-dotenv
# numpy pandas

# Instale o Runtime Interface Client (RIC) da AWS Lambda
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
    --target ${FUNCTION_DIR}

# Imagem final com Python Alpine
FROM python-alpine

# Defina o diretório de trabalho
ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}

# Copie a aplicação do estágio de build
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Baixe e configure o AWS Lambda Runtime Interface Emulator (RIE) para execução local
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/download/v1.22/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY entry.sh /
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh
RUN chmod 755 /entry.sh


# Defina o ponto de entrada e o comando da função Lambda
ENTRYPOINT [ "/entry.sh" ]
CMD [ "lambda_function.lambda_handler" ]