# 数据的持久化操作redis---->MongoDB
import redis
from pymongo import MongoClient
import json

# 爬虫实现简单分布式：多个url放到列表里，往里不停放URL，程序循环取值，
# 可以把url放到redis中，多台机器从redis中取值，爬取数据，实现简单分布式

# 实例化redis客户端
redis_client = redis.Redis(host='127.0.0.1', port=6379)
# 实例化MongoDB客户端
mongo_client = MongoClient(host='127.0.0.1', port=27017)

# 指定链接的MongDB数据库、集合
db = mongo_client['jdbook']
col = db['jdbook']
# 使用循环把redis中数据全部写入到MongoDB中

while True:
    # 从redis中取出数据
    key, data = redis_client.blpop(['jdbook:items'])
    print('key', key)
    print('data',data)
    #json.loads()函数是将json格式数据转换为字典
    # 把数据写入到MongoDB中
    col.insert_one(json.loads(data.decode()))


# 关闭数据库
mongo_client.close()