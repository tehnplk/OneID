import requests
import time
import pymysql
from pymysql.constants import CLIENT

url = """https://phr1.moph.go.th/idp/api/check_ekyc"""
auth_token = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZWhucGxrQDAwMDUxIiwiaWF0IjoxNzEwNTkzOTA3LCJleHAiOjE3MTA2NzY3MDcsImlzcyI6Ik1PUEggQWNjb3VudCBDZW50ZXIiLCJhdWQiOiJNT1BIIEFQSSIsImNsaWVudCI6eyJ1c2VyX2lkIjozNDY4MCwidXNlcl9oYXNoIjoiMjlGMEQzRTY0ODlFM0ZCMkFGNDlBQzZCMkUxOUUyMTE3RTQ1OEVGNEVFRUQyMEJFNDRDMTNEMTgzREUxRTAwRDhDQ0NGMEFBMTQiLCJsb2dpbiI6InRlaG5wbGsiLCJuYW1lIjoi4LiZ4Liy4Lii4Lit4Li44LmA4LiX4LiZIOC4iOC4suC4lOC4ouC4suC4h-C5guC4l-C4mSIsImhvc3BpdGFsX25hbWUiOiLguKrguLPguJnguLHguIHguIfguLLguJnguKrguLLguJjguLLguKPguJPguKrguLjguILguIjguLHguIfguKvguKfguLHguJTguJ7guLTguKnguJPguLjguYLguKXguIEiLCJob3NwaXRhbF9jb2RlIjoiMDAwNTEiLCJlbWFpbCI6InBsa3Byb21AZ21haWwuY29tIiwiYWNjb3VudF9hY3RpdmF0ZWQiOnRydWUsImFjY291bnRfc3VzcGVuZGVkIjpmYWxzZSwibGFzdF9jaGFuZ2VfcGFzc3dvcmQiOjE3MDk2NDU1ODEsImxhc3RfY29uZmlybV9vdHAiOjE3MTA1OTEwMzUsImNpZF9oYXNoIjoiNEFGMEFGODNGRjdEQkI3Q0JFMEEwNEFDRjEyNTY2QzI6MzciLCJjaWRfZW5jcnlwdCI6IjQ4NjQ4QjU2MkQ2NTY2QUJFOUZBNTIyOUVENjUwNEUxMjY3NDk3REE4OUE1N0FDNjJGODdFMzQyM0YyNTZEQTUzQjUyNTg3QUZGQjk2ODVBQUYxNTVDMTZEMiIsImNpZF9hZXMiOiIxaGExcFNrYVJkME9sR1hrbGhKRWlRPT0iLCJjbGllbnRfaXAiOiI0OS4yMjguMTE4LjkxIiwic2NvcGUiOlt7ImNvZGUiOiJBUFBPSU5UTUVOVF9EQVNIQk9BUkQ6MSJ9LHsiY29kZSI6Ik1PUEhfSURQX0FETUlOOjEifSx7ImNvZGUiOiJNT1BIX0lEUF9BUEk6MSJ9LHsiY29kZSI6Ik1PUEhfQUNDT1VOVF9DRU5URVJfQURNSU46MyJ9LHsiY29kZSI6IkFQUE9JTlRNRU5UX0FQSTozIn0seyJjb2RlIjoiTU9QSF9QSFJfSElFOjMifSx7ImNvZGUiOiJNT1BIX1BIUl9ISUU6MyJ9LHsiY29kZSI6Ik1PUEhfRk9SRUlHTl9JRFA6MyJ9LHsiY29kZSI6Ik1PUEhfSURQX0FETUlOOjMifSx7ImNvZGUiOiJNT1BIX0lEUF9BRE1JTjozIn0seyJjb2RlIjoiTU9QSF9JRFBfQURNSU46MyJ9LHsiY29kZSI6Ik1PUEhfSURQX0FQSTozIn0seyJjb2RlIjoiTU9QSF9JRFBfQVBJOjMifSx7ImNvZGUiOiJNT1BIX0NMQUlNOjMifSx7ImNvZGUiOiJNT1BIX0NMQUlNX0FQSTozIn0seyJjb2RlIjoiTU9QSF9DTEFJTV9BRE1JTjozIn0seyJjb2RlIjoiTU9QSF9QSFJfVklFVzozIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX1ZJRVc6MSJ9LHsiY29kZSI6IklNTVVOSVpBVElPTl9VUERBVEU6MSJ9LHsiY29kZSI6Ik1PUEhfQUNDT1VOVF9DRU5URVJfQURNSU46MSJ9LHsiY29kZSI6IklNTVVOSVpBVElPTl9QRVJTT05fVVBMT0FEOjEifSx7ImNvZGUiOiJJTU1VTklaQVRJT05fREFTSEJPQVJEOjEifSx7ImNvZGUiOiJJTU1VTklaQVRJT05fU0xPVDoxIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX1FVT1RBOjEifSx7ImNvZGUiOiJJTU1VTklaQVRJT05fTEFCOjEifSx7ImNvZGUiOiJJTU1VTklaQVRJT05fU0xPVF9NQU5BR0VSOjEifSx7ImNvZGUiOiJFUElERU1fVVBEQVRFREFUQToxIn0seyJjb2RlIjoiRVBJREVNX1JFUE9SVDoxIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX1JFUE9SVF9FWENFTDoxIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX0VQSURFTToxIn0seyJjb2RlIjoiTU9QSF9QSFJfSElFOjEifSx7ImNvZGUiOiJNT1BIX0ZPUkVJR05fSURQOjEifSx7ImNvZGUiOiJNT1BIX1BIUl9EQVNIQk9BUkQ6MSJ9LHsiY29kZSI6Ik1PUEhfUEhSX0RBU0hCT0FSRF9SRVBPUlQ6MSJ9LHsiY29kZSI6Ik1PUEhfQ0xBSU06MSJ9LHsiY29kZSI6Ik1PUEhfQ0xBSU1fQVBJOjEifSx7ImNvZGUiOiJNT1BIX0NMQUlNX0FETUlOOjEifSx7ImNvZGUiOiJJTU1VTklaQVRJT05fVklFVzoyIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX1VQREFURToyIn0seyJjb2RlIjoiTU9QSF9BQ0NPVU5UX0NFTlRFUl9BRE1JTjoyIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX1BFUlNPTl9VUExPQUQ6MiJ9LHsiY29kZSI6IklNTVVOSVpBVElPTl9EQVNIQk9BUkQ6MiJ9LHsiY29kZSI6IklNTVVOSVpBVElPTl9RVU9UQToyIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX1JFUE9SVDoyIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX1JFUE9SVF9FWENFTDoyIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX0NPTVBBTlk6MiJ9LHsiY29kZSI6IklNTVVOSVpBVElPTl9BRUZJX1VQREFURToyIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX0RJU1RSSUNUX0NPTVBBTlk6MiJ9LHsiY29kZSI6IklNTVVOSVpBVElPTl9DT01QQU5ZOjMifSx7ImNvZGUiOiJJTU1VTklaQVRJT05fVklFVzozIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX0RBU0hCT0FSRDozIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX0FETUlOOjMifSx7ImNvZGUiOiJJTU1VTklaQVRJT05fUkVQT1JUOjMifSx7ImNvZGUiOiJJTU1VTklaQVRJT05fTEFCOjMifSx7ImNvZGUiOiJJTU1VTklaQVRJT05fRVBJREVNOjMifSx7ImNvZGUiOiJFUElERU1fVVBEQVRFREFUQTozIn0seyJjb2RlIjoiRVBJREVNX1JFUE9SVDozIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX1VQREFURTozIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX1BFUlNPTl9VUExPQUQ6MyJ9LHsiY29kZSI6IklNTVVOSVpBVElPTl9RVU9UQTozIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX1JFUE9SVF9FWENFTDozIn0seyJjb2RlIjoiSU1NVU5JWkFUSU9OX1NMT1RfTUFOQUdFUjozIn0seyJjb2RlIjoiTU9QSF9QSFJfREFTSEJPQVJEX1JFUE9SVDozIn1dLCJyb2xlIjpbIm1vcGgtYXBpIl0sInNjb3BlX2xpc3QiOiJbQVBQT0lOVE1FTlRfREFTSEJPQVJEOjFdW01PUEhfSURQX0FETUlOOjFdW01PUEhfSURQX0FQSToxXVtNT1BIX0FDQ09VTlRfQ0VOVEVSX0FETUlOOjNdW0FQUE9JTlRNRU5UX0FQSTozXVtNT1BIX1BIUl9ISUU6M11bTU9QSF9QSFJfSElFOjNdW01PUEhfRk9SRUlHTl9JRFA6M11bTU9QSF9JRFBfQURNSU46M11bTU9QSF9JRFBfQURNSU46M11bTU9QSF9JRFBfQURNSU46M11bTU9QSF9JRFBfQVBJOjNdW01PUEhfSURQX0FQSTozXVtNT1BIX0NMQUlNOjNdW01PUEhfQ0xBSU1fQVBJOjNdW01PUEhfQ0xBSU1fQURNSU46M11bTU9QSF9QSFJfVklFVzozXVtJTU1VTklaQVRJT05fVklFVzoxXVtJTU1VTklaQVRJT05fVVBEQVRFOjFdW01PUEhfQUNDT1VOVF9DRU5URVJfQURNSU46MV1bSU1NVU5JWkFUSU9OX1BFUlNPTl9VUExPQUQ6MV1bSU1NVU5JWkFUSU9OX0RBU0hCT0FSRDoxXVtJTU1VTklaQVRJT05fU0xPVDoxXVtJTU1VTklaQVRJT05fUVVPVEE6MV1bSU1NVU5JWkFUSU9OX0xBQjoxXVtJTU1VTklaQVRJT05fU0xPVF9NQU5BR0VSOjFdW0VQSURFTV9VUERBVEVEQVRBOjFdW0VQSURFTV9SRVBPUlQ6MV1bSU1NVU5JWkFUSU9OX1JFUE9SVF9FWENFTDoxXVtJTU1VTklaQVRJT05fRVBJREVNOjFdW01PUEhfUEhSX0hJRToxXVtNT1BIX0ZPUkVJR05fSURQOjFdW01PUEhfUEhSX0RBU0hCT0FSRDoxXVtNT1BIX1BIUl9EQVNIQk9BUkRfUkVQT1JUOjFdW01PUEhfQ0xBSU06MV1bTU9QSF9DTEFJTV9BUEk6MV1bTU9QSF9DTEFJTV9BRE1JTjoxXVtJTU1VTklaQVRJT05fVklFVzoyXVtJTU1VTklaQVRJT05fVVBEQVRFOjJdW01PUEhfQUNDT1VOVF9DRU5URVJfQURNSU46Ml1bSU1NVU5JWkFUSU9OX1BFUlNPTl9VUExPQUQ6Ml1bSU1NVU5JWkFUSU9OX0RBU0hCT0FSRDoyXVtJTU1VTklaQVRJT05fUVVPVEE6Ml1bSU1NVU5JWkFUSU9OX1JFUE9SVDoyXVtJTU1VTklaQVRJT05fUkVQT1JUX0VYQ0VMOjJdW0lNTVVOSVpBVElPTl9DT01QQU5ZOjJdW0lNTVVOSVpBVElPTl9BRUZJX1VQREFURToyXVtJTU1VTklaQVRJT05fRElTVFJJQ1RfQ09NUEFOWToyXVtJTU1VTklaQVRJT05fQ09NUEFOWTozXVtJTU1VTklaQVRJT05fVklFVzozXVtJTU1VTklaQVRJT05fREFTSEJPQVJEOjNdW0lNTVVOSVpBVElPTl9BRE1JTjozXVtJTU1VTklaQVRJT05fUkVQT1JUOjNdW0lNTVVOSVpBVElPTl9MQUI6M11bSU1NVU5JWkFUSU9OX0VQSURFTTozXVtFUElERU1fVVBEQVRFREFUQTozXVtFUElERU1fUkVQT1JUOjNdW0lNTVVOSVpBVElPTl9VUERBVEU6M11bSU1NVU5JWkFUSU9OX1BFUlNPTl9VUExPQUQ6M11bSU1NVU5JWkFUSU9OX1FVT1RBOjNdW0lNTVVOSVpBVElPTl9SRVBPUlRfRVhDRUw6M11bSU1NVU5JWkFUSU9OX1NMT1RfTUFOQUdFUjozXVtNT1BIX1BIUl9EQVNIQk9BUkRfUkVQT1JUOjNdIiwiYWNjZXNzX2NvZGVfbGV2ZWwxIjoiJyciLCJhY2Nlc3NfY29kZV9sZXZlbDIiOiInJyIsImFjY2Vzc19jb2RlX2xldmVsMyI6Iic2NTAwMDAnIiwiYWNjZXNzX2NvZGVfbGV2ZWw0IjoiJyciLCJhY2Nlc3NfY29kZV9sZXZlbDUiOiInJyJ9fQ.oiznVEbSrKXvnKLsrdQAuSfMCOWXJwQ8oAzCFcjRrrCRXojbqLBTWr1H5_kokuMFWDFwsZna-S-8sVwLMaZzPhgBr-Yqlr7i3tguM6lqDuc7dNbUPPEGaQEFFnLzY09CpcCKTBhlIOsia1DZ2vXoCHR-Tle43hWDK4vi__A3L7wMV3yWcnm-YlmEAicpyHWUU1kY41X7YA5mKg4Qu45ukRqec5GOXKNTMfIiuJthfjk9mYh5m15fN4svCQS-D8edoiaClndnGWEboMGO8JgHeQhcvT3dkFlT8lskiZq5Lp_h5-cszfqX8uTF0CP2Mw2ldUXCcenDWMOtAEPBt9zl5UBYwROEa9TT3s1w_WPjFDyWGgw5xKjeTH1_1Lt-XYqJBqLeLKfsgS6HUUhrZWZzrDGyJFyEPbrh2XG5JCoj6uvevAubdT1WJrT-2YL8JXjATBh3XQaT7WrhrP5OAC9-HAmoy2EzRTRJ-wz2kPGGSb0br4YRUMjwr_CChgvALhicEjhfSuXqjgSO_-DyCPRED6Vcg9GHsctF6Ivc9ODXRDeBlQkzG0tXMw9AC5jK6YWUcXfjynLlsW55qJ5Ci3ooIKT1pOZs0Rhcd3Mv9STw6V3GM3iSzF8t4DOUHQJOfUo4LD4CU7GvTt2y24uLCC1f6hbj11uYWcCLKQxJVWQosAU"
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



sql = "select * from plk_moph_id_person_check";
cur.execute(sql)
persons = cur.fetchall()
i = 0
for p in persons:
    i += 1
    c = p['cid']
    data = {'cid': c}
    response = requests.post(url, json=data, headers=headers)
    print(i, c, response.json())
    time.sleep(.25)



