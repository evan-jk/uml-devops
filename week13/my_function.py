import os
import json
import pymysql
import csv

def my_function():
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

  try:
    conn = pymysql.connect(host=host,user=user,password=pw,db=db,port=port)
    m_query = """SELECT * FROM Orders;"""
    local_filename = "/root/mount_file/test.csv"

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


