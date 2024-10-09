import os
import csv
import json
import boto3
import requests
from time import sleep
from datetime import datetime
import pymysql
# import datetime

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
        road_name = s3_key.split("_")[-1].replace(".csv", "")
        
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

        db_process = save_metrics_to_db(metrics=metrics, road_name=road_name)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "success lambda 2",
                "metrics": metrics,
                "db_process": db_process
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


def save_metrics_to_db(metrics, road_name):
    try:
        db_host = os.getenv('host')
        db_user = os.getenv('user')
        db_password = os.getenv('password')
        db_database = os.getenv('database')
        db_port = int(os.getenv('port'))
        # Conectar ao banco de dados
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_database,
            port=db_port,
        )

        with connection.cursor() as cursor:
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            for vehicle, number_deaths in metrics.items():
                if vehicle == "total_geral":
                    continue  # Ignorar o total

                # Verificar se já existe um registro para este road_name e vehicle
                if record_exists(cursor, road_name, vehicle):
                    update_record(cursor, created_at, number_deaths, road_name, vehicle)
                else:
                    insert_record(cursor, created_at, road_name, vehicle, number_deaths)

            connection.commit()

        # Retornar um JSON de sucesso
        return {"status": "success", "message": "Metrics saved successfully"}

    except pymysql.MySQLError as e:
        # Tratamento de erro com retorno de JSON detalhando a falha
        return {"status": "error", "message": str(e)}

    finally:
        if connection:
            connection.close()

# Função para verificar se o registro já existe
def record_exists(cursor, road_name, vehicle):
    check_sql = "SELECT id FROM road_incidents WHERE road_name = %s AND vehicle = %s"
    cursor.execute(check_sql, (road_name, vehicle))
    return cursor.fetchone() is not None

# Função para atualizar o registro existente
def update_record(cursor, created_at, number_deaths, road_name, vehicle):
    update_sql = """
        UPDATE road_incidents 
        SET created_at = %s, number_deaths = %s 
        WHERE road_name = %s AND vehicle = %s
    """
    cursor.execute(update_sql, (created_at, number_deaths, road_name, vehicle))

# Função para inserir um novo registro
def insert_record(cursor, created_at, road_name, vehicle, number_deaths):
    insert_sql = """
        INSERT INTO road_incidents (created_at, road_name, vehicle, number_deaths)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_sql, (created_at, road_name, vehicle, number_deaths))