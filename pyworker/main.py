import redis
import os
import io

def load_words_into_redis(redis, words):
    print("Loading words")
    count = 0
    first_word = ""
    for word in words:
        redis.mset({word:"true"})
        count += 1
        if first_word == "":
            first_word = word

        if count % 1000 == 0:
            print(str(count) + "words loaded - first - '" + first_word + "' last - '" + word + "'")
            first_word = ""

    print("Finished")


if __name__ == '__main__':
    server_url = "0.0.0.0"    
    server_port = int("6379")    
    if 'SERVER_URL' in os.environ:
        server_url = os.environ['SERVER_URL']
    if 'SERVER_PORT' in os.environ:
        server_port = int(os.environ['SERVER_PORT'])

    redis = redis.Redis(host=server_url, port=server_port)

    with(io.open("./word-list.txt")) as f:
        words = [line.rstrip() for line in f]

    load_words_into_redis(redis, words)

