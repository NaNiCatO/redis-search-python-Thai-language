# Redis Search Python (for Thai language)

This project is a Python implementation of Redis search functionality. It allows you to perform full-text search operations on data stored in Redis for Thai language text.

## Search Service gRPC Overview

This project provides a gRPC service for a search engine using Redis and Redisearch. The service includes the following functionalities:
- SayHello: A simple greeting service.
- Query: A search query service that returns results based on the provided query.
- StreamQuery: A streaming search query service that continuously processes queries and returns results.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Configuration](#configuration)


## Installation <a id='installation'></a>

### Prerequisites

- Python 3.7 or later
- pip (Python package installer)
- Redis server

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

>generating the gRPC code
>```
>python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. search.proto
>```

## Example <a id='example'></a>

### testing grpc server
> service SayHello
>```python
>import grpc
>
># Import the generated classes for our protocol buffer message and service definitions.
>import search_pb2
>import search_pb2_grpc
>
># Function to call the SayHello RPC method.
>def say_hello(stub, name):
>    # Create a HelloRequest message and Call the SayHello method on the stub (client)
>    response = stub.SayHello(search_pb2.HelloRequest(name=name))
>    print(f"SayHello response: {response.message}")
>
>def main():
>    # Create an insecure gRPC channel to the server running on localhost at port 50051.
>    with grpc.insecure_channel('localhost:50051') as channel:
>         # Create a stub (client) for the SearchService using the channel.
>         stub = search_pb2_grpc.SearchServiceStub(channel)
>
>    say_hello(stub, 'World')
>```
![say_hello](/image/query-service.png)  

### Unary RPCs
client sends a single request to the server and gets a single response back
> service Query
>```python
>import grpc
>
># Import the generated classes for our protocol buffer message and service definitions.
>import search_pb2
>import search_pb2_grpc
>
># Function to call the Query RPC method.
>def query(stub, query, page, limit):
>    # Create a QueryRequest message and Call the SayHello method on the stub (client)
>    response = stub.Query(search_pb2.QueryRequest(query=query, page=page, limit=limit))
>
>    print(f"Query response: {response.total_hits} hits")
>    for doc in response.items:
>        print(f"Document: {doc.name}, {doc.location}")
>
>def main():
>    # Create an insecure gRPC channel to the server running on localhost at port 50051.
>    with grpc.insecure_channel('localhost:50051') as channel:
>         # Create a stub (client) for the SearchService using the channel.
>         stub = search_pb2_grpc.SearchServiceStub(channel)
>
>   query(stub, 'example', 1, 10)
>```
![query](/image/query-service.png)  

### Bidirectional streaming RPCs
the server wait to receive all the client messages before writing its responses
> service StreamQuery list of request
>```python
>import grpc
>
># Import the generated classes for our protocol buffer message and service definitions.
>import search_pb2
>import search_pb2_grpc
>
># Function to call the StreamQuery RPC method with streaming requests.
>def stream_query(stub, queries):
>    # Inner generator function to yield QueryRequest messages for each query.
>    def query_iterator():
>        for q in queries:
>            yield search_pb2.QueryRequest(query=q['query'], page=q['page'], limit=q['limit'])
>
>    # Call the StreamQuery method on the stub (client) with the query_iterator generator.
>    for response in stub.StreamQuery(query_iterator()):
>        print(f"StreamQuery response: {response.total_hits} hits")
>        for doc in response.items:
>            print(f"Document: {doc.name}, {doc.location}")
>
>def main():
>    # Create an insecure gRPC channel to the server running on localhost at port 50051.
>    with grpc.insecure_channel('localhost:50051') as channel:
>         # Create a stub (client) for the SearchService using the channel.
>         stub = search_pb2_grpc.SearchServiceStub(channel)
>
>        # List of queries to send to the StreamQuery method.
>        queries = [
>            {'query': 'โรงเรียน', 'page': 0, 'limit': 10},
>            {'query': 'โรงแรม', 'page': 0, 'limit': 10}
>        ]
>        stream_query(stub, queries)
>```
![stream_query_v1](/image/steamquery-v1-service.png)  

### Bidirectional streaming RPCs
the server alternately read a message then write a message
> service StreamQuery continuously ask the user for input
>```python
>import grpc
>
># Import the generated classes for our protocol buffer message and service definitions.
>import search_pb2
>import search_pb2_grpc
>
># Function to continuously prompt the user for queries and stream responses from the server.
>def loop_query(stub):
>    # Inner generator function to yield QueryRequest messages based on user input.
>    def query_iterator():
>        print("Enter your query (or type 'exit' to stop): ")
>        while True:
>            query = input()
>            if query.lower() == 'exit':
>                break
>            yield search_pb2.QueryRequest(query=query, page=0, limit=10)
>
>    # Call the StreamQuery method on the stub (client) with the query_iterator generator.
>    for response in stub.StreamQuery(query_iterator()):
>        print(f"StreamQuery response: {response.total_hits} hits")
>        for doc in response.items:
>            print(f"Document: {doc.name}, {doc.location}")
>
>def main():
>    # Create an insecure gRPC channel to the server running on localhost at port 50051.
>    with grpc.insecure_channel('localhost:50051') as channel:
>         # Create a stub (client) for the SearchService using the channel.
>         stub = search_pb2_grpc.SearchServiceStub(channel)
>
>        loop_query(stub)
>```
![stream_query_v2](/image/steamquery-v2-service.png)  

## Config <a id='configuration'></a>
algorithm to tokenize thai words before sending to redis server  
- `ver.py`  

setting of query type to send to redis server  
- `search_data.py`  

config massage and grpc services
- `search.proto`
Generate gRPC code from the `search.proto` file:
```sh
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. search.proto
```

For more information on how to use the Redis Search Python library, please refer to the [documentation](https://github.com/redislabs/redisearch-py).  
For more information on how to use the gPRC Python library, please refer to the [documentation](https://github.com/grpc/grpc).

## Performance Benchmark
To measure the performance of the gRPC server, we use tools ghz to load test the server.  
**test case:**
- total: 1000
- stream-interval: 0
**request message**
{
  "query": "โรงเรียน",
  "page": 1,
  "limit": 10
}
**result**
- total hit: 20000+

# Synchronous server
**Query service**
| concurrency 1 | concurrency 10 |
|:-------------:|:--------------:|
|    24.24 ms   |    164.68 ms   |

**SteamQuery service**
| concurrency 1 | concurrency 10 |
|:-------------:|:--------------:|
|    24.24 ms   |    164.68 ms   |

# asynchronous server
**Query service**
| concurrency 1 | concurrency 10 |
|:-------------:|:--------------:|
|    23.16 ms   |    202.83 ms   |

**SteamQuery service**
| concurrency 1 | concurrency 10 |
|:-------------:|:--------------:|
|    23.37 ms   |    208.39 ms   |


## Citations
This project utilizes concepts and technologies from the following sources:
- [gRPC Core Concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)
- [Redis Search and Query](https://redis.io/docs/latest/develop/interact/search-and-query/)
- [gRPC Performance Guide](https://grpc.io/docs/guides/performance/)
- [N-gram on Wikipedia](https://en.wikipedia.org/wiki/N-gram)

## Contributions
I am the sole contributor to this project. Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.