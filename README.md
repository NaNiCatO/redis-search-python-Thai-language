# Redis Search Python (for Thai language)

This project is a Python implementation of Redis search functionality. It allows you to perform full-text search operations on data stored in Redis for Thai language text.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Installation <a id='installation'></a>

To install the Redis Search Python library, you can use pip:

```
pip install redisearch
```

To install the grpc Python library, use pip:

```
pip install grpc
```

Deploying Redis with the RediSearch module in Docker

>Pull the Image:
>```
>docker pull redislabs/redisearch:latest
>```

>Run the Container:
>```
>docker run -d --name redisearch -p 6379:6379 redislabs/redisearch:latest
>```


## Usage <a id='usage'></a>

Here's a simple example of how to use the Redis Search Python:

>For grpc server connect to redis server
>```
>python server.py # synchronous grpc server
>python async server.py # asynchronous grpc server
>```

>For load data to redis server
>```
>python load_data.py
>```

>For simple app implementation
>```
>python pyqt_app.py
>```

>Connecting grpc client to grpc server
>```python
>import search_pb2
>import search_pb2_grpc
>
>grpc_channel = grpc.insecure_channel('localhost:50051')
>stub = search_pb2_grpc.SearchServiceStub(self.grpc_channel)
>```

>grpc services
>in the `search.proto`

## Config <a id='configuration'></a>
algorithm to tokenize thai words before sending to redis server  
-ver.py  


setting of query type to send to redis server  
-search_data.py  
  


For more information on how to use the Redis Search Python library, please refer to the [documentation](https://github.com/redislabs/redisearch-py).
For more information on how to use the gPRC Python library, please refer to the [documentation](https://github.com/grpc/grpc).
