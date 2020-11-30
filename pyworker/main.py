import redis

if __name__ == '__main__':
    r = redis.Redis(host='0.0.0.0', port=6379)
    r.mset({"key1":"value1"})
    pass
