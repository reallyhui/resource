# -*- coding: utf8 -*-
import pymysql
import random, string

code = string.digits + string.ascii_letters

# 随机生成,n表示生成验证码n组，生成m组码
def to_code(m, n):
    a = ""
    for i in range(m):
        for j in range(n):
            b = "".join(random.sample(code, 5))
            if j == n - 1:
                a = a + b
            else:
                a = a + b + '-'
        to_mysql(a,i)
        a = ""

def to_mysql(a, i):

    conn = pymysql.connect(user='root', password='root', database='code')
    cursor = conn.cursor()
    cursor.execute('show tables')
    tb_list = []
    for tb in cursor.fetchall():
        tb_list.append(tb[0])
    if 'code' not in tb_list:
        cursor.execute('create table code(id VARCHAR(20) PRIMARY KEY ,code VARCHAR(200))')
    cursor.execute('insert into code(id,code) values(%s,%s)', [i, a])
    cursor.rowcount
    conn.commit()
    conn.close()


if __name__ == '__main__':
    to_code(200, 5)
