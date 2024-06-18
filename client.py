import grpc
import search_pb2
import search_pb2_grpc

def say_hello(stub, name):
    response = stub.SayHello(search_pb2.HelloRequest(name=name))
    print(f"SayHello response: {response.message}")

def query(stub, query, page, limit):
    response = stub.Query(search_pb2.QueryRequest(query=query, page=page, limit=limit))
    print(f"Query response: {response.total_hits} hits")
    for doc in response.items:
        print(f"Document: {doc.name}, {doc.location}")

def stream_query(stub, queries):
    def query_iterator():
        for q in queries:
            yield search_pb2.QueryRequest(query=q['query'], page=q['page'], limit=q['limit'])
    
    for response in stub.StreamQuery(query_iterator()):
        print(f"StreamQuery response: {response.total_hits} hits")
        for doc in response.items:
            print(f"Document: {doc.name}, {doc.location}")

def loop_query(stub):
    def query_iterator():
        print("Enter your query (or type 'exit' to stop): ")
        while True:
            query = input()
            if query.lower() == 'exit':
                break
            yield search_pb2.QueryRequest(query=query, page=0, limit=10)

    for response in stub.StreamQuery(query_iterator()):
        print(f"StreamQuery response: {response.total_hits} hits")
        for doc in response.items:
            print(f"Document: {doc.name}, {doc.location}")

def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = search_pb2_grpc.SearchServiceStub(channel)
        
        # Call SayHello method
        say_hello(stub, 'World')
        
        # Call Query method
        query(stub, 'โรงเรียน', 0, 10)
        
        # Call StreamQuery method
        queries = [
            {'query': 'โรงเรียน', 'page': 0, 'limit': 10},
            {'query': 'โรงแรม', 'page': 0, 'limit': 10}
        ]
        stream_query(stub, queries)

        # Loop Query
        loop_query(stub)

if __name__ == '__main__':
    main()
