# README.md
A little demonstration of using REDIS with persistence on docker-compose.  

Consists of a Redis cache and Worker container.  The worker will read a value from the cache, overwrite the value and then wait for a small period of time. 

## Prereqs 
Requires:
* docker - 18.09.2
* docker-compose - 1.23.1

Tested on MacOS and Ubuntu 18.04.

## Running
To run the example simply run the following and watch the logs in the console.  

```
docker-compose up --build
```

The first time you run you will see something like this 

```
redis-worker_1_c9571969d9ae | DATE_WITH_TIME=
redis-worker_1_c9571969d9ae | OK
redis-worker_1_c9571969d9ae | DATE_WITH_TIME=20190430-211558
redis-worker_1_c9571969d9ae | OK
redis-worker_1_c9571969d9ae | DATE_WITH_TIME=20190430-211618
redis-worker_1_c9571969d9ae | OK
```

Second time you run it will show the last stored value - indicating persistence. 

```
redis-worker_1_c9571969d9ae | DATE_WITH_TIME=20190430-211638
```

## Development
Use vscode - 
vscode
shellcheck


## Redis

[Commands](https://redis.io/commands)  
