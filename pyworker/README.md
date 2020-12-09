# pyworker
Working through this [guide](https://realpython.com/python-redis/)

## Setup

```
export PIPENV_VENV_IN_PROJECT=1
pipenv install --three
```

## Manual setup and work

```sh
# run redis and cli container.
docker-compose -f ./docker-compose.yaml up 

# insert some data 
python ./main.py   

# run a client to query
docker run -it --rm --network=pyworker_redis_backplane --entrypoint /bin/sh redis:5.0.4-alpine

# connect inside the container
> redis-cli -h redis

# shuld see 1) "true"
> mget aardvark
```


