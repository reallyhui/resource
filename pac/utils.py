#-*- coding:utf-8
from pymysql import connect
from functools import wraps
import random,time,os,json,pandas as pd
UA_MAP={
    "PC":"Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 74.0.3729.131Safari / 537.36",
    "Phone":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}
MYSQL_CONFIG = dict(
        host="127.0.0.1" ,#mysql所在服务器ip
        port = 3306, #端口
        user = "root" ,#用户名
        password = "root",#密码
        database = "graduate", #数据库名
        charset = "utf8" #字符集
)
def extra_first(xpath_res: list):
    """对xpath的结果进行解析    strip()前后去空白"""
    return xpath_res[0].strip() if xpath_res and xpath_res[0] else None
def is_file_exist(file_name):
    """判断文件是否存在"""
    if os.path.exists(file_name):
        os.remove(file_name)
def wait(func):
    """请求休眠装饰函数"""
    def wrapper(*args,**kwargs):
        #sec的范围1.0到2.0  休眠时间
        sec = round(random.random()+1,2)
        print(f'请求休眠：{sec}s')
        time.sleep(sec)
        return func(*args,**kwargs)
    return wrapper

def json2csv(file_name:str):
    """将json格式文件转换成csv文件"""
    with open(file_name, encoding="utf8") as f:
        datas = [json.loads(line[:-2]) for line in f]
    pd.DataFrame(datas).to_csv(file_name.replace("json","csv"),encoding="gbk",index=False)

def count_time(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start = time.time()
        res = func(*args,**kwargs)
        end = time.time()
        print(f"{func.__name__} 执行耗时：{round(end-start,2)}")
        return res
    return wrapper

@count_time
def json2sql(file_name:str):
    """将jsong格式文件数据插入数据库"""
    # 1.创建连接对象
    conn = connect(**MYSQL_CONFIG)
    # 2.获取cursor
    cur = conn.cursor()
    # 3.进行C(create)U(update)R(read)D(delete)
    with open(file_name, encoding="utf8") as f:
        datas = [json.loads(line[:-2]) for line in f]
    try:
        for data in datas:
            insert_sql = """
            insert into dacheng values (0,"{name}","{detail_url}","{email}","{position}","{location}");
            """.format(
                name=data["name"],
                detail_url=data["detail_url"],
                email=data["email"],
                position=data["position"],
                location=data["location"]
            )
            cur.execute(insert_sql)
            conn.commit()
    except Exception as why:
        print(why)
        print("--" * 30)
        print(insert_sql)
    finally:
        # 4.关闭资源(遵循穿脱原则)
        cur.close()
        conn.close()

"""多行插入"""
@count_time
def json2sqltwo(file_name:str):
    """将jsong格式文件数据插入数据库"""
    # 1.创建连接对象
    conn = connect(**MYSQL_CONFIG)
    # 2.获取cursor
    cur = conn.cursor()
    # 3.进行C(create)U(update)R(read)D(delete)
    with open(file_name, encoding="utf8") as f:
        datas = [json.loads(line[:-2]) for line in f]
    try:
        exe_sql = """insert into dacheng values"""
        for data in datas:
            insert_sql = """
            (0,"{name}","{detail_url}","{email}","{position}","{location}"),
            """.format(
                name=data["name"],
                detail_url=data["detail_url"],
                email=data["email"],
                position=data["position"],
                location=data["location"]
            )
            exe_sql += insert_sql
        exe_sql = exe_sql.strip()[:-1] + ";"
        cur.execute(exe_sql)
        conn.commit()
    except Exception as why:
        print(why)
        print("--" * 30)
        print(exe_sql)
    finally:
        # 4.关闭资源(遵循穿脱原则)
        cur.close()
        conn.close()


if __name__ == '__main__':
    # print(json2sql.__name__)
    json2sql("dacheng.json")