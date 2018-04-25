import os

#连接mysql数据库，根据spiderlevel和gain_time字段将url添加到redis里
MYSQL_SETTINGS = {
    'host': os.getenv('MYSQL_HOST','10.245.144.72'),
    'user': os.getenv('MYSQL_USER','root'),
    'passwd': os.getenv('MYSQL_PASSWD','root'),
    'db': [
        'information_schema',
        os.getenv('MYSQL_DB','APTDatabase'),
    ],
    'table': [os.getenv('MYSQL_TABLE','sitelistnew1'),
              ],
    'port': int(os.getenv('MYSQL_PORT',3306))
}

#将url添加到redis里
REDIS_SETTINGS = {
    'host': os.getenv('REDIS_HOST','10.245.144.94'),
    'port': int(os.getenv('REDIS_HOST',6379)),
    'password': os.getenv('REDIS_PASSWORD','HITdbManager-rw!')
}
#django服务数据库，存着图片的名字，计算每天的爬取数量
MYSQL_DJANGO_SETTINGS = {
    'host': os.getenv('MYSQL_DJANGO_HOST','10.245.144.91'),
    'user': os.getenv('MYSQL_DJANGO_USER','root'),
    'passwd': os.getenv('MYSQL_DJANGO_PASSWD','nslab'),
    'db': [
        'information_schema',
        os.getenv('MYSQL_DJANGO_DB','testware'),
    ],
    'table': [
              os.getenv('MYSQL_DJANGO_TABLE1','midapp_img'),
              os.getenv('MYSQL_DJANGO_TABLE2','everyday_num'),
              ],
    'port': int(os.getenv('MYSQL_DJANGO_PORT',3306))
}