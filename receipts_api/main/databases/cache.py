import redis


cache = redis.StrictRedis(
    host='redis',
    port=6379,
    password=''
)


def check_key(dict):
    return cache.hgetall(dict)


def add_key(key, rec_num, reg_num, date, total):
    receipt = {
        'rec_num': rec_num,
        'reg_num': reg_num,
        'total': f'{total}',
        'date': f'{date}'        
    }
    return cache.hmset(key, receipt)
