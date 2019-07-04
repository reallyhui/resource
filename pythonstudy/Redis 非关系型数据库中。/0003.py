# -*- coding: utf8 -*-

import random, string
import redis

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
        print(a)
        r.set(i, a)
        a = ""


# 存入非关系型数据库Redis
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

if __name__ == '__main__':
    to_code(200, 5)
