import redis
import pymysql
import time
import datetime
from settings import MYSQL_SETTINGS,REDIS_SETTINGS
#/home/zrq/PycharmProjects/aptnote/aptnote.py
def Mysqlconnect(mysqlsetting,database_id):
    '''
    连接mysql数据库
    :param database: (int)指定的数据库，在settings.py查看
    :return db: 数据库链接
    '''
    db = pymysql.connect(
        host=mysqlsetting['host'],
        user=mysqlsetting['user'],
        passwd=mysqlsetting['passwd'],
        db=mysqlsetting['db'][database_id],
        port=mysqlsetting['port'])
    return db

def Redisconnect():
    '''
    链接redis
    :return r:redis链接
    '''
    r = redis.Redis(
        host=REDIS_SETTINGS['host'],
        port=REDIS_SETTINGS['port'],
        password=REDIS_SETTINGS['password'])
    return r

def Gettablerows(mysqlsetting, database, tablename):
    '''
    计算database数据库中table表的记录数
    :return numbers: (int)表中记录数
    '''
    db = Mysqlconnect(mysqlsetting,0)
    cur = db.cursor()
    sql = "SELECT table_rows FROM TABLES WHERE TABLE_SCHEMA ='"+database+"' AND table_name='"+tablename+"'"
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            numbers = row[0]
        print(numbers)
    except Exception as e:
        raise e
    db.close()
    return numbers

def Getnowdate():
    '''
    获取当前日期
    :return [date_now,date2]: 当前时间的两种格式
    '''
    date_now = datetime.datetime.now().strftime('%Y/%m/%d')
    date2 = time.strptime(date_now, "%Y/%m/%d")
    return [date_now,date2]

def Caltime(date1,date2):
    '''
    计算两个日期相差天数
    :param date1: 由gain_time字段获取上一次爬取url的日期
    :param date2: 当前日期
    :return: (int)两个日期相差天数
    '''
    date1 = time.strptime(date1, "%Y/%m/%d")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    return (date2-date1).days

def Urlqueue(url_number, date, tablename):
    '''
    找出需要加入队列的url，存入redis，更新gain_time字段
    :param url_number: 表中的url数目
    :param date: 当前日期
    :return:
    '''
    #格式化spiderlevel对应天数
    ttime=[0,1,7,30,90,180]
    db = Mysqlconnect(MYSQL_SETTINGS,1)
    cur = db.cursor()
    r=Redisconnect()

    for id in range(1, url_number):
        sql="SELECT real_url, spiderlevel, gain_time FROM "+tablename+" WHERE id="+str(id)
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                real_url=row[0]
                spiderlevel=row[1]
                gain_time=row[2]
                datedevi=Caltime(str(gain_time), date[1])

                if (datedevi>ttime[int(spiderlevel)]):

                    r.sadd('url_list', real_url)

                    sql="UPDATE "+tablename+" SET gain_time='"+str(date[0])+"' WHERE id="+str(id)
                    cur.execute(sql)
                    db.commit()


        except Exception as e:
            raise e
    db.close()

    status='OK'
    print(date[0], status)

def add_to_redis():
    tablename=MYSQL_SETTINGS['table'][1]
    db = Mysqlconnect(MYSQL_SETTINGS, 1)
    cur = db.cursor()
    r = Redisconnect()
    sql = "SELECT get_url FROM " + tablename
    cur.execute(sql)
    results = cur.fetchall()
    for row in results:
        real_url = row[0]
        r.sadd('url_list', real_url)

if __name__ == '__main__':
    mysqlsetting=MYSQL_SETTINGS

    databasename = mysqlsetting['db'][1]
    tablename = mysqlsetting['table'][0]

    #获取表中记录数
    url_number = Gettablerows(mysqlsetting, databasename, tablename)
    # 获取当前date
    date = Getnowdate()
    Urlqueue(url_number, date, tablename)
