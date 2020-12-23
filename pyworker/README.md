# pyworker
Working through this [guide](https://realpython.com/python-redis/)

## Setup

```
export PIPENV_VENV_IN_PROJECT=1
pipenv install --three
```

## Manual setup and test

```sh
# run redis and cli container.
docker-compose -f ./docker-compose.yaml up 

# insert some data 
python ./main.py   

# run a client to query
docker run -it --rm --network=pyworker_redis_backplane --entrypoint /bin/sh redis:5.0.4-alpine

# connect inside the container
> redis-cli -h redis

# get version information
> info server

# shuld see 1) "true"
> mget aardvark
```

## Run python cli to load and query data
Examples for the pyworker cli
```sh
# flush the cache
python ./main.py flush  

# insert the dictionary 
python ./main.py load --method slice 

# get info on redis server
python ./main.py query --method info           

# get info on key
python ./main.py query --method key --key aardvark

# scan all keys matching a pattern
python ./main.py query --method scan --match "b*"   
```





