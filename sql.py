# 直接运行该脚本可创建相应数据库
from os import pathsep
import mysql.connector
import copy
from rexrules import Rules
from config import SQL_CONFIG

# 连接数据库
def connect(conf):
    try:
        cnx = mysql.connector.connect(**conf)
    except mysql.connector.Error as err:
        print(err)
    else:
        return cnx

# 创建数据库waf
def initsql_waf():
    config = copy.copy(SQL_CONFIG)
    config.pop('database')
    conn = connect(config)
    cursor = conn.cursor()

    try:
        cursor.execute("SHOW DATABASES")
    except mysql.connector.Error as err:
        print(err)

    database = cursor.fetchall()

    if ('waf',) in database:
        pass
    else:
        print("创建数据库waf")
        try:
            cursor.execute("CREATE DATABASE waf")
            conn.commit()
        except mysql.connector.Error as err:
            print(err)

    cursor.close()
    conn.close()


# 创建rule表
def initsql_rule(Rules):
    conn = connect(SQL_CONFIG)
    cursor = conn.cursor()

    # rule表
    table_sql = """
    CREATE TABLE `rule`  (
    `id` varchar(255) NOT NULL,
    `name` varchar(255) NOT NULL,
    `rex` varchar(255) NOT NULL,
    `timestamp` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `type` varchar(255) NOT NULL,
    `risk_level` varchar(255) NOT NULL,
    PRIMARY KEY (`id`));
    """

    # 插入rule
    insert_sql = """
    INSERT INTO `rule` (`id`,`name`,`rex`,`type`,`risk_level`) VALUES (UUID(),%s,%s,%s,%s)
    """

    #查询表
    try:
        cursor.execute("SHOW TABLES")
    except mysql.connector.Error as err:
        print(err)

    tables = cursor.fetchall()

    # 创建rule表
    if ('rule',) in tables:
        pass
    else:
        print("创建表rule")
        try:
            cursor.execute(table_sql)
        except mysql.connector.Error as err:
            print(err)
        for rule in Rules:
            insert_data = (rule, Rules[rule]['rex'], Rules[rule]['name'], Rules[rule]['risk_level'])
            try:
                cursor.execute(insert_sql,insert_data)
                conn.commit()
            except mysql.connector.Error as err:
                print(err)

    cursor.close()
    conn.close()

def initsql_log():
    conn = connect(SQL_CONFIG)
    cursor = conn.cursor()

    table_sql = """
    CREATE TABLE `log`  (
    `id` int NOT NULL AUTO_INCREMENT,
    `path` varchar(255) NOT NULL,
    `timestamp` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`));
    """

    try:
        cursor.execute("SHOW TABLES")
    except mysql.connector.Error as err:
        print(err)

    tables = cursor.fetchall()

    # 创建rule表
    if ('log', ) in tables:
        pass
    else:
        print("创建表log")
        try:
            cursor.execute(table_sql)
        except mysql.connector.Error as err:
            print(err)

    cursor.close()
    conn.close()


def insert_log(fileaddr):
    conn = connect(SQL_CONFIG)
    cursor = conn.cursor()

    insert_sql = """
    INSERT INTO `log` (`path`) VALUES (%s)
    """

    try:
        cursor.execute("SELECT path FROM log")
    except mysql.connector.Error as err:
        print(err)
    paths = cursor.fetchall()
    if (fileaddr,) not in paths:
        try:
            cursor.execute(insert_sql,(fileaddr,))
            conn.commit()
        except mysql.connector.Error as err:
            print(err)
    cursor.close()
    conn.close()

# 查询waf规则
def query_rule():
    Rules = {}
    conn = connect(SQL_CONFIG)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name, type, rex, risk_level FROM rule")
    except mysql.connector.Error as err:
        print(err)

    result = cursor.fetchall()

    for rule in result:
        Rules[rule[0]] = {"name": rule[1], "rex": rule[2], "risk_level": rule[3]}

    cursor.close()
    conn.close()
    return Rules

if __name__ == '__main__':
    initsql_waf()
    initsql_rule(Rules)
    initsql_log()