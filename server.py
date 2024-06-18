import grpc
from concurrent import futures
import search_pb2 as search_pb2
import search_pb2_grpc as search_pb2_grpc
from redis import Redis
from redisearch import Client
from redis.exceptions import RedisError
import time

# Import the search_name function
from scripts.search_data import search_name

class SearchService(search_pb2_grpc.SearchServiceServicer):
    def __init__(self):
        try:
            self.redis_client = Redis(host='localhost', port=6379)
            self.client = Client('myIndex', conn=self.redis_client)
        except RedisError as e:
            print(f"Failed to connect to Redis: {e}")
            raise

    def SayHello(self, request, context):
        return search_pb2.HelloResponse(message=f"Hello, {request.name}!")

    def Query(self, request, context):
        try:

            items, total_hits = search_name(request.query, self.client, request.page, request.limit)
            documents = [search_pb2.Document(name=item.name, location=item.location) for item in items]
            
            print(f"Total hits: {total_hits}")
            
            return search_pb2.QueryResponse(total_hits=total_hits, items=documents)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return search_pb2.QueryResponse(total_hits=0, items=[])

        
    def StreamQuery(self, request_iterator, context):
        try:
            for request in request_iterator:
                try:
                    start = time.time()
                    items, total_hits = search_name(request.query, self.client, request.page, request.limit)
                    
                    end = time.time()
                    print(f"Total hits: {total_hits}")
                    
                    documents = [search_pb2.Document(name=item.name, location=item.location) for item in items]
                    yield search_pb2.QueryResponse(total_hits=total_hits, items=documents)
                except Exception as e:
                    print(f"Error processing query: {e}")
                    context.set_details(str(e))
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    yield search_pb2.QueryResponse(total_hits=0, items=[])
        except Exception as e:
            print(f"Stream error: {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            yield search_pb2.QueryResponse(total_hits=0, items=[])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    search_pb2_grpc.add_SearchServiceServicer_to_server(SearchService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    print("Starting gRPC server...")
    serve()
