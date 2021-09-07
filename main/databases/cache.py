import redis


cache = redis.StrictRedis(
    host='redis',
    port=6379,
    password=''
)


def check_key(key):
    return cache.hgetall(key)


def add_key(key, receipt_num, registration_num, created_at, total):
    receipt = {
        'receipt_num': receipt_num,
        'registration_num': registration_num,
        'total': f'{total}',
        'created_at': f'{created_at}'        
    }
    return cache.hmset(key, receipt)
