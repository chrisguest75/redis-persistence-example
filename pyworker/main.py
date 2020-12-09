import redis
import os
import io

if __name__ == '__main__':
    server_url = "0.0.0.0"    
    server_port = int("6379")    
    if 'SERVER_URL' in os.environ:
        server_url = os.environ['SERVER_URL']
    if 'SERVER_PORT' in os.environ:
        server_port = int(os.environ['SERVER_PORT'])

    redis = redis.Redis(host=server_url, port=server_port)

    with(io.open("./word-list.txt")) as f:
        lines = [line.rstrip() for line in f]

    print("Loading words")
    count = 0
    for word in lines:
        redis.mset({word:"true"})
        count += 1
        if count % 1000 == 0:
            print(count, "words loaded" )

    print("Finished")


