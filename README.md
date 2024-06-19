# Redis Search Python (for Thai language)

This project is a Python implementation of Redis search functionality. It allows you to perform full-text search operations on data stored in Redis for Thai language text.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
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

## Config <a id='configuration'></a>
algorithm to tokenize thai words before sending to redis server  
-ver.py  


setting of query type to send to redis server  
-search_data.py  
  


For more information on how to use the Redis Search Python library, please refer to the [documentation](https://github.com/redislabs/redisearch-py).  
For more information on how to use the gPRC Python library, please refer to the [documentation](https://github.com/grpc/grpc).
