import os
import sys
import requests
import time
import pymysql
from pymysql.constants import CLIENT

def update_check(cid, resp, cur, conn):
    msg = str(resp['Message']).replace("'", "")
    result = str(resp['result']).replace("'", "")
    sql = f"update plk_moph_id_person_check set last_check_at = NOW(),last_message = '{msg}',moph_id_check_result = '{result}' where cid = '{cid}'"
    # print(sql)
    cur.execute(sql)
    conn.commit()
    print(f'update for {cid}')


def read(txt):
    with open(txt, 'r') as f:
        r = f.read()
        return r;

if __name__ == '__main__':
    url = """https://phr1.moph.go.th/idp/api/check_ekyc"""
    auth_token = read('./token.txt')
    headers = {'Authorization': f'Bearer {auth_token}'}

    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '112233',
        'db': 'hos',
        'port': 3306,
        'charset': 'tis620'
    }

    conn = pymysql.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'].encode("utf-8"),
        db=config['db'],
        port=config['port'],
        charset=config['charset'],
        client_flag=CLIENT.MULTI_STATEMENTS,
        autocommit=False, )

    cur = conn.cursor(pymysql.cursors.DictCursor)

    sql_create = read('./sql_create.sql')
    cur.execute(sql_create);
    conn.commit();

    sql = """select * from plk_moph_id_person_check 
             where moph_id_check_result = '0' AND date(last_check_at) <> CURDATE()""";

    sql = """select * from plk_moph_id_person_check 
                 where moph_id_check_result = '0' """;
    cur.execute(sql)
    persons = cur.fetchall()
    n = len(persons)
    i = 0
    for p in persons:
        i += 1
        cid = p['cid']
        data = {'cid': cid}
        response = requests.post(url, json=data, headers=headers)
        resp = response.json()
        print(f"{i}/{n}", ' --> ', cid, resp)
        if resp['MessageCode'] == 200:
            update_check(cid, resp, cur, conn)

    # time.sleep(.25)