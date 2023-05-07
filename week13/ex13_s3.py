import os
import json
import pymysql
import csv
import boto3
import configparser

def csv_function():
  for key, value in os.environ.items():
    print(f"{key}: {value}")

  mysql_conn = os.environ.get("AIRFLOW_CONN_MY_MYSQL")
  print(mysql_conn)
  json_dict = json.loads(mysql_conn)
  user = json_dict['user']
  pw = json_dict['password']
  host = json_dict['host']
  db = json_dict['database']
  port = int(json_dict['port'])
  local_filename = "/root/mount_file/week13-ekerekanich.csv"

  try:
    conn = pymysql.connect(host=host,user=user,password=pw,db=db,port=port)
    m_query = """SELECT * FROM Orders;"""
    
    m_cursor = conn.cursor()
    m_cursor.execute(m_query)
    results = m_cursor.fetchall()

    with open(local_filename, 'w') as fp:
      csv_w = csv.writer(fp, delimiter='|')
      csv_w.writerows(results)
      print(results)

    m_cursor.close()
    conn.close()
  except Exception as e:
    print(e)
    traceback.print_exc()
    sys.exit(1)

def s3_function():
  for key, value in os.environ.items():
    print(f"{key}: {value}")

  s3_conn = os.environ.get("S3_CONN")
  print(s3_conn)
  json_dict = json.loads(s3_conn)
  access = json_dict['access']
  secret = json_dict['secret']
  local_filename = "/root/mount_file/week13-ekerekanich.csv"

  try:
    s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    s3_file = 'week13-ekerekanich.csv'
    s3.upload_file(local_filename, 'UML', s3_file)
  except Exception as e:
    print(e)
    traceback.print_exc()
    sys.exit(1)
  