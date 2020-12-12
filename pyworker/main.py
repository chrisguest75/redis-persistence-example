import redis
import os
import io
import time 

# TODO:
# Timing outputs
# Load as a list
# Load with less requests
# Pickle?
# Read out values to build a dictionary

def load_words_into_redis(redis, words):
    '''
    Load words into redis as keys - slow.......
    '''
    print("Loading words")
    count = 0
    first_word = ""
    for word in words:
        redis.mset({word:"true"})
        count += 1
        if first_word == "":
            first_word = word

        if count % 1000 == 0:
            print(str(count) + " words loaded - first - '" + first_word + "' last - '" + word + "'")
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

    # load the word list
    start = time.perf_counter()
    filepath = "./word-list.txt"
    print(f"Load file '{filepath}'")
    with(io.open(filepath)) as f:
        words = [line.rstrip() for line in f]
    print(f"Time taken to load file '{time.perf_counter() - start:0.4f}' secs")

    # push into redis
    start = time.perf_counter()
    load_words_into_redis(redis, words)
    print(f"Time taken to load words into Redis '{time.perf_counter() - start:0.4f}' secs")

