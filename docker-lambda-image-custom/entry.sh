#!/bin/sh

# Captura o sinal de interrupção e termina o script corretamente
trap "exit" SIGINT SIGTERM

if [ -z "$AWS_LAMBDA_RUNTIME_API" ]; then
    /usr/bin/aws-lambda-rie python${RUNTIME_VERSION} -m awslambdaric $1
else
    python${RUNTIME_VERSION} -m awslambdaric $1
fi