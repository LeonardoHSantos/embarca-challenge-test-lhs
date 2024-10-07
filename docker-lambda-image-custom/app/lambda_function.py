import os
import csv
import json
import boto3
import requests
from time import sleep
from datetime import datetime

# Inicializar cliente S3
s3 = boto3.client('s3')
bucket_name = os.getenv('bucket_name')

def lambda_handler(event, context):

    try:
        body = json.loads(event["body"])
    except:
        body = event
    
    save_file = lambda_1(body, context)
    if save_file["statusCode"] == 200:
        resume_file = lambda_2(body, context)
        return resume_file
    
    return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'error test lambda python',
            })
        }


def lambda_1(event, context):

    try:

        # Obter o link do CSV do evento
        csv_url = event.get('csv_url')

        print(f">>>> csv_url: {csv_url}")
        
        # Fazer o download do arquivo CSV
        response = requests.get(csv_url)
        csv_content = response.content.decode(encoding="latin-1").replace("\n", "")

        # Salvar o CSV no S3
        s3_key = event.get("csv_url").split("/")[-1]
        s3.put_object(Body=csv_content, Bucket=bucket_name, Key=s3_key)
        
        return {
            'statusCode': 200,
            's3_key': s3_key
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "event": event,
            }),
            "function": "lambda_1",
            "error": str(e)
        }

def lambda_2(event, context):
    try:
        # Obter o s3_key da Lambda 1
        s3_key = event.get("csv_url").split("/")[-1]
        
        # Baixar o CSV do S3
        response = s3.get_object(Bucket=bucket_name, Key=s3_key, )
        csv_content = response['Body'].read().decode('utf-8').splitlines()

        # Utilizado em testes local
        # with open(s3_key, "r") as f:
        #     csv_content = f.read().splitlines()

        headers = csv_content[0].replace("\n", "").split(";")
        csv_content.pop(0)

        metrics = {
            "total_geral": 0,
            "automovel": 0,
            "bicicleta": 0,
            "caminhao": 0,
            "moto": 0,
            "onibus": 0,
        }
        for row in csv_content:
            data = row.split(";")
            print(data)
            for i in range(len(headers)):
                if headers[i] in metrics.keys():
                    n = int(data[i])
                    metrics[headers[i]] += n
                    metrics["total_geral"] += n

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "success lambda 2",
                "metrics": metrics,
            })
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "event": event,
            }),
            "function": "lambda_2",
            "error": str(e)
        }