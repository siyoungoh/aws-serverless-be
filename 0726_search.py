import json
import boto3
import pymysql
from datetime import date
import math


def get_secret():
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="ap-northeast-2"
    )
    get_secret_value_response = client.get_secret_value(
        SecretId='rds-secret-02'
    )
    token = get_secret_value_response['SecretString']
    return eval(token)


def db_ops():
    secrets = get_secret()
    try:
        connection = pymysql.connect(
            host=secrets['host'],
            user=secrets['username'],
            password=secrets['password'],
            db='sparta',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    except pymysql.MySQLError as e:
        print("connection error!!")
        return e

    print("connection ok!!")
    return connection


def lambda_handler(event, context):
    param_type = event['queryStringParameters']['type']
    conn = db_ops()
    cursor = conn.cursor()

    try:
        if param_type == 'write':
            if event['httpMethod'] == 'OPTIONS':
                body = json.dumps({
                    "message": "success",
                })
            else:
                today = date.today()
                body = json.loads(event['body'])
                conn = db_ops()
                cursor = conn.cursor()
                cursor.execute("insert into bbs(title, content, regDate) value('" + body['title'] + "', '" + body[
                    'content'] + "', '" + today.strftime("%Y%m%d") + "')")
                conn.commit()
                body = json.dumps({
                    "message": "success",
                })
        elif param_type == 'list':
            param_word = event['queryStringParameters']['word']

            if not param_word:
                cursor.execute("select idx, title, regDate from bbs")
                result = cursor.fetchall()
            else:
                cursor.execute("select idx, title, regDate from bbs where title like '%" + param_word + "%'")
                result = cursor.fetchall()

            body = json.dumps({
                "result": "success",
                "data": result
            })
        elif param_type == 'read':
            idx = event['queryStringParameters']['idx']
            cursor.execute("select * from bbs where idx=" + idx)
            bbs = cursor.fetchone()
            body = json.dumps({
                "result": "success",
                "data": bbs
            })
        elif param_type == 'delete':
            idx = event['queryStringParameters']['idx']
            cursor.execute("delete from bbs where idx=" + idx)
            conn.commit()
            body = json.dumps({
                "message": "success",
            })

        return {
            "statusCode": 200,
            # Cross Origin처리
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "body": body,
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            # Cross Origin 처리
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "body": json.dumps({
                "message": "fail",
            }),
        }
