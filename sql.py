import mysql.connector
from config import sqlconfig

# 连接数据库
def connect(conf):
    try:
        cnx = mysql.connector.connect(**conf)
    except mysql.connector.Error as err:
        print(err)
    else:
        return cnx

# 创建规则数据库
def initrulesql(Rules):
    conn = connect(sqlconfig)
    cursor = conn.cursor()
    
    table_sql = """
    CREATE TABLE `rule`  (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `rex` varchar(255) NOT NULL,
    `timestamp` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `type` varchar(255) NOT NULL,
    `risk_level` varchar(255) NOT NULL,
    PRIMARY KEY (`id`));
    """

    insert_sql = """
    INSERT INTO `rule` (`name`,`rex`,`type`,`risk_level`) VALUES (%s,%s,%s,%s)
    """

    try:
        cursor.execute("SHOW TABLES")
    except mysql.connector.Error as err:
        print(err)
    tables = cursor.fetchone()
    # 创建数据库
    if "rule" in tables:
        pass
    else:
        print("创建数据库")
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


# 查询waf规则
def query_rule():
    Rules = {}
    conn = connect(sqlconfig)
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