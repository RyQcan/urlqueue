import pymysql
import time
import datetime
from settings import MYSQL_MISSION_SETTINGS
from aptnote import Mysqlconnect,Gettablerows


def Update_mission(today_number):
    db = Mysqlconnect(MYSQL_MISSION_SETTINGS,1)
    cur = db.cursor()
    tablename=MYSQL_MISSION_SETTINGS['table'][1]
    sql = "SELECT number FROM "+tablename+" where id=1"
    cur.execute(sql)
    results = cur.fetchall()
    for row in results:
        yesterday_number = row[0]
    today_compnum=today_number-yesterday_number
    sql = "INSERT INTO "+tablename+" (number,date)VALUES("+str(today_compnum)+",now())"
    cur.execute(sql)
    db.commit()
    db.close()

if __name__ == '__main__':
    mysqlsetting=MYSQL_MISSION_SETTINGS
    databasename = mysqlsetting['db'][1]
    tablename = mysqlsetting['table'][0]
    # 获取表中记录数

    today_number = Gettablerows(mysqlsetting, databasename, tablename)

    Update_mission(today_number)