import redis
import os
import io
import time 
from code_timer import CodeTimer
import argparse
import pprint

# TODO:
# Load with less requests
# Pickle?
# Read out values to build a dictionary

def load_words_into_redis_mset(redis, words):
    '''
    Load words into redis as keys - slow.......
    '''
    ct = CodeTimer()    

    print(f"Loading {len(words)} words")
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

def load_words_into_redis_mset_slice(redis, words):
    '''
    Load words into redis as sliced chunks - slow.......
    '''
    ct = CodeTimer()    

    print(f"Loading {len(words)} words")
    count = 0
    grab = 5000
    ct.start()
    while count < len(words):
        take = grab
        if count + grab > len(words):
            take = len(words) - count        
        sliced = words[count:(take + count)]
        count += take

        bag = {}
        for word in sliced:
            bag[word] = "true"   
        redis.mset(bag)

        print(f"{count} words loaded - first:'{sliced[0]}' last:'{sliced[-1]}' '{ct.stop():0.4f}' secs")
        ct.start()

    ct.stop()
    print("Finished")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Redis dataload example')
    parser.add_argument('--server', default="0.0.0.0", dest='server', type=str, help='')
    parser.add_argument('--port', default="6379", dest='port', type=str, help='')


    parser.add_argument('action', choices=['load', 'flush', 'query', 'watch'])

    # load
    parser.add_argument('--method', dest='method', type=str, help='Name of method for data loading')

    # flush

    # query
    parser.add_argument('--key', dest='key', type=str, help='Name of key to query')
    parser.add_argument('--match', dest='match', type=str, help='Pattern to match when querying strings')


    args = parser.parse_args()

    server_url = args.server   
    server_port = int(args.port)    
    if 'SERVER_URL' in os.environ:
        server_url = os.environ['SERVER_URL']
    if 'SERVER_PORT' in os.environ:
        server_port = int(os.environ['SERVER_PORT'])

    print(f"{server_url}:{server_port}")
    redis = redis.Redis(host=server_url, port=server_port)

    ############################################################
    # load
    ############################################################
    if args.action == "load":
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
        if args.method == None:
            load_words_into_redis_mset(redis, words)
        elif args.method.lower() == "slice":
            load_words_into_redis_mset_slice(redis, words)
        else:
            print(f"Method {args.method} not recognised")
        print(f"Time taken to load words into Redis '{ct.stop():0.4f}' secs")

    ############################################################
    # flush
    ############################################################
    if args.action == "flush":
        preflush=redis.dbsize()
        redis.flushdb()
        postflush=redis.dbsize()
        print(f"Flushed dbsize:{preflush} - now {postflush}" )

    ############################################################
    # query
    ############################################################
    if args.action == "query":
        if args.method == None:
            print("No method specified - try info")
        elif args.method.lower() == "info":
            print(f"dbsize:{redis.dbsize()}")
            print(f"client_id:{redis.client_id()}")
            print(f"client_list:{redis.client_list()}")
            print(f"lastsave:{redis.lastsave()}")
            pprint.pprint(f"memory_stats:{redis.memory_stats()}")
            print(f"time:{redis.time()}")            
        elif args.method.lower() == "key":
            if args.key != None:
                print(f"key:{args.key} value:{redis.mget(args.key)}")
                print(f"strlen:{redis.strlen(args.key)}")
                print(f"ttl:{redis.ttl(args.key)}")
            else:
                print("No key specified")
        elif args.method.lower() == "scan":
            words = 0
            match = "*" if args.match == None else args.match
            for key in redis.scan_iter(match=match,count=1000):
                words += 1
                print(key)
            print(f"{words} in set")
            #keys = redis.scan(cursor=0, match=".", count=1000, _type="SET")
            #print(keys)
        else:
            print(f"Method {args.method} not recognised")

    ############################################################
    # watch
    ############################################################
    if args.action == "watch":
        pubsub = redis.pubsub()
        pubsub.psubscribe('__keyspace@0__:*')
        print('Starting message loop')
        while True:
            message = pubsub.get_message()
            if message:
                print(message)
            else:
                time.sleep(0.01)

