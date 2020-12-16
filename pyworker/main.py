import redis
import os
import io
import time 
from code_timer import CodeTimer
import argparse

# TODO:
# Load as a list
# Load with less requests
# Pickle?
# Read out values to build a dictionary

def load_words_into_redis(redis, words):
    '''
    Load words into redis as keys - slow.......
    '''
    ct = CodeTimer()    

    print("Loading words")
    count = 0
    first_word = ""
    ct.start()
    for word in words:
        redis.mset({word:"true"})
        count += 1
        if first_word == "":
            first_word = word

        if count % 1000 == 0:
            print(f"{count} words loaded - first:'{first_word}' last:'{word}' '{ct.stop():0.4f}' secs")
            first_word = ""
            ct.start()

    print(f"{count} words loaded - first:'{first_word}' last:'{word}' '{ct.stop():0.4f}' secs")
    print("Finished")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Redis dataload example')
    parser.add_argument('--method', dest='method', type=str, help='Name of method for data loading')
    parser.add_argument('--server', default="0.0.0.0", dest='server', type=str, help='')
    parser.add_argument('--port', default="6379", dest='port', type=str, help='')

    args = parser.parse_args()

    server_url = args.server   
    server_port = int(args.port)    
    if 'SERVER_URL' in os.environ:
        server_url = os.environ['SERVER_URL']
    if 'SERVER_PORT' in os.environ:
        server_port = int(os.environ['SERVER_PORT'])

    print(f"{server_url}:{server_port}")
    redis = redis.Redis(host=server_url, port=server_port)

    # load the word list
    ct = CodeTimer()    
    ct.start()
    filepath = "./word-list.txt"
    print(f"Load file '{filepath}'")
    with(io.open(filepath)) as f:
        words = [line.rstrip() for line in f]   
    print(f"Time taken to load file '{ct.stop():0.4f}' secs")

    # push into redis
    ct.start()
    load_words_into_redis(redis, words)
    print(f"Time taken to load words into Redis '{ct.stop():0.4f}' secs")

